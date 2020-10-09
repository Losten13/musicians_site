from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication

from lessons.models import Lesson
from lessons.permissions import IsOwner
from lessons.serializers import LessonSerializer

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

    @action(detail=True, methods=['put'], name='upvote')
    def upvote(self, request,  pk=None):
        lesson = self.get_object()
        serializer = self.get_serializer(lesson,data = request.data,partial=True )
        serializer.is_valid()
        serializer.save(votes=lesson.votes + 1)
        return Response(serializer.data)