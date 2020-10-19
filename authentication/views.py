
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from authentication.serializers import RegisterSerializer
from authentication.task import send_registration_email


class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        '''
        post:
        Register new user
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        email_template = 'email/email.html'
        subject = 'Registration'
        send_registration_email.delay(user.email, email_template, subject)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
