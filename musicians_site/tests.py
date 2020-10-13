from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User


class APITestUser(APITestCase):

    def create_user(self, email, password):
        user = User.objects.create_user(email, password)
        user.is_active = True
        user.save()
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {token}", **additional_headers
        )

    def create_and_authorize(self, email, password, **additional_headers):
        user = self.create_user(email, password)
        self.authorize(user, **additional_headers)
        return user

