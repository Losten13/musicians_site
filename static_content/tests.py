
# Create your tests here.
from rest_framework import status
from rest_framework.reverse import reverse

from rest_framework.test import APITestCase

from musicians_site.utils import generate_photo_file


class TestImageUploadView(APITestCase):

    def setUp(self):
        self.image = generate_photo_file()

    def test_upload_image(self):
        response = self.client.post(reverse('image'), data=self.image, content_type='image/*')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

