from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authentication.serializers import RegisterSerializer, UserSerializer
from authentication.task import send_registration_email


class RegisterApi(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        send_registration_email.delay(user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
