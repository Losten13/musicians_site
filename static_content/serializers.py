
from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField(read_only=True)
