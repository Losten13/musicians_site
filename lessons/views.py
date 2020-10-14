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


class LessonViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    filterset_fields = ['creator']

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], url_path='toggle-like')
    def toggle_like(self, request, *args, **kwargs):
        lesson = self.get_object()
        try:
            Vote.objects.get(voted=request.user.id, lesson=lesson.id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Vote.DoesNotExist:
            vote = Vote.objects.create(voted=request.user, lesson=lesson)
            vote.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


class VoteViewSet(viewsets.ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
