import io
import tempfile

from django.test import TestCase

from PIL import Image
# Create your tests here.
from rest_framework.reverse import reverse
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

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self) -> None:
        self.create_and_authorize('a@gmail.com', '123qwe123', )

    def test_register(self):
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)
        tmp_file.seek(0)

        img = self.generate_photo_file()
        data = {'email': 'a@gmail.com', 'password': '123qwe123', 'avatar_img': tmp_file}
        response = self.client.post(reverse('auth_register'), data=data, format='multipart')
        print(response)
        self.assertEqual(response.status_code, 201)
