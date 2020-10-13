import io
import tempfile
from unittest.mock import patch

from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.test import TestCase

from PIL import Image
# Create your tests here.
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings

from rest_framework_simplejwt.tokens import AccessToken

from authentication.models import User
from musicians_site.tests import APITestUser


class TestRegisterView(APITestUser):

    def setUp(self) -> None:
        self.email = 'test11@gmail.com'
        self.password = '123qwe123'


    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    @patch('authentication.task.send_registration_email.delay')
    def test_register(self, delay):
        img = self.generate_photo_file()

        with default_storage.open(img.name, 'wb') as f:
            f.write(img.getvalue())

        data = {'email': self.email, 'password': self.password, 'avatar_img': img.name}
        response = self.client.post(reverse('auth-register'), data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], self.email)
        created_user = User.objects.get(email=self.email)
        self.assertTrue(check_password(self.password, created_user.password))
        delay.assert_called_once()

    def test_register_wrong_email(self):
        pass
