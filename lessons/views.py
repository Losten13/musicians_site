from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.models import User
from lessons.models import Lesson, Vote
from lessons.permissions import IsOwner
from lessons.serializers import LessonSerializer, VoteSerializer

from rest_framework.response import Response


class LessonList(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['post'], name='match')
    def match(self, request):
        user_id = request.data['user_id']
        try:
            user = User.objects.get(pk=user_id)  # TODO try block
            user_lessons = Lesson.objects.filter(creator=user)
            serializer = self.get_serializer(data=user_lessons, many=True)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'msg': 'Object doe not exist'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], name='upvote')
    def upvote(self, request, pk=None):
        lesson = self.get_object()
        try:
            vote = Vote.objects.get(voted=request.user.id, lesson=lesson.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            vote = Vote.objects.create(voted=request.user, lesson=lesson)
            vote.save()
            serializer = VoteSerializer(vote)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class VoteView(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
