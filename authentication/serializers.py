from django.db import transaction
from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'avatar_img')


class RegisterSerializer(serializers.ModelSerializer):
    avatar_img = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'avatar_img')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['email'],
            validated_data['password'],
        )
        user.avatar_img.name = validated_data['avatar_img']
        user.save()
        return user
