from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authentication.serializers import RegisterSerializer, UserSerializer
from authentication.task import send_registration_email


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        email_template = 'email/email.html'
        subject = 'Registration'
        send_registration_email.delay(user.email, email_template, subject)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
