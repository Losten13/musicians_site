from rest_framework import serializers, validators

from authentication.models import User
from .models import Lesson


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class LessonSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_url', 'creator', 'votes')
