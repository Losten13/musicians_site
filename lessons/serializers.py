from django.db import transaction
from rest_framework import serializers, validators


from .models import Lesson, Vote


class LessonSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    votes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    lesson_img = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_url', 'creator', 'votes', 'lesson_img')


class VoteSerializer(serializers.ModelSerializer):
    voted = serializers.PrimaryKeyRelatedField(read_only=True)
    lesson = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'lesson', 'voted', 'is_voted')

