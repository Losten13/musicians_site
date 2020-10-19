from unittest.mock import patch

from django.contrib.auth.hashers import check_password

from rest_framework.reverse import reverse

from authentication.models import User
from musicians_site.tests import APITestUser


class TestRegisterView(APITestUser):

    def setUp(self) -> None:
        self.email = 'test11@gmail.com'
        self.password = '123qwe123'
        self.img_name = 'Test.jpeg'

    @patch('authentication.task.send_registration_email.delay')
    def test_register(self, delay):
        data = {'email': self.email, 'password': self.password, 'avatar_img': self.img_name}
        response = self.client.post(reverse('auth-register'), data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['email'], self.email)
        created_user = User.objects.get(email=self.email)
        self.assertTrue(check_password(self.password, created_user.password))
        delay.assert_called_once()

    def test_register_wrong_email(self):
        pass
