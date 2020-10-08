from rest_framework import  serializers

from authentication.models import User
from .models import Lesson


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ('id', 'email',)
        read_only_field = ('id',)



class LessonSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Lesson
        field = ('id', 'title', 'video_url', 'user')
        read_only_field = ('id',)

