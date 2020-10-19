from django.utils.decorators import method_decorator
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.models import Subscription, Author
from authentication.serializers import SubscriptionSerializer
from lessons.models import Lesson, Vote
from lessons.pagination import ResultSetPagination
from lessons.permissions import IsOwner
from lessons.serializers import LessonSerializer
from django.http import JsonResponse

from rest_framework.response import Response

from lessons.task import send_notify_email


@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    auto_schema=None
))
class LessonViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    filterset_fields = ['creator']
    pagination_class = ResultSetPagination

    def perform_create(self, serializer):
        """Create lessons"""
        try:
            author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            author = Author(user=self.request.user)
            author.save()

        author_subscriptions = Subscription.objects.filter(author=author)
        if author_subscriptions.count() > 0:
            subscribers_emails = []
            for subscription in author_subscriptions:
                subscribers_emails.append(subscription.subscriber.email)
            email_template = 'email/notify.html'
            subject = 'Notification'
            send_notify_email.delay(subscribers_emails, email_template, subject)

        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], url_path='toggle-like',
            permission_classes=[permissions.IsAuthenticatedOrReadOnly, ])
    def toggle_like(self, request, *args, **kwargs):
        '''
        post:
        Toggle like for lesson
        '''

        lesson = self.get_object()
        try:
            Vote.objects.get(voted=request.user.id, lesson=lesson.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voted=request.user, lesson=lesson)
            vote.save()
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='subscribe',
            permission_classes=[permissions.IsAuthenticatedOrReadOnly, ])
    def subscribe(self, request, *args, **kwargs):
        '''
        post:
        Subscribe to author of current lessons
        '''
        lesson = self.get_object()
        author = Author.objects.get(user=lesson.creator)
        new_sub = Subscription(author=author, subscriber_id=request.user.id)
        new_sub.save()
        return Response(status=status.HTTP_201_CREATED)


class UserSubscriberView(ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        '''
        get:
        Get subscribes of current user
        '''
        subs = self.queryset.filter(author=request.user.id).values()
        serializer = SubscriptionSerializer(data=subs)
        serializer.is_valid()
        return JsonResponse({'subs': list(subs)})
