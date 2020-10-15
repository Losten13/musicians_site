from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.models import Subscription, Author, User
from lessons.models import Lesson, Vote
from lessons.permissions import IsOwner
from lessons.serializers import LessonSerializer, VoteSerializer

from rest_framework.response import Response

from lessons.task import send_notify_email
from musicians_site.utils import upload_to


class LessonViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    filterset_fields = ['creator']

    def perform_create(self, serializer):
        try:
            author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            author = Author(user=self.request.user)
            author.save()

        author_subscriptions = Subscription.objects.filter(author=author)
        if author_subscriptions.count() > 0:
            print(author_subscriptions)
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
        lesson = self.get_object()
        author = Author.objects.get(user=lesson.creator)
        new_sub = Subscription(author=author, subscriber_id=request.user.id)
        new_sub.save()
        return Response(status=status.HTTP_201_CREATED)


class VoteViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
