from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from drf_yasg2.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from static_content.parsers import ImageUploadParser
from static_content.serializers import ImageUploadSerializer
from static_content.utils import resize_image, bytes_from_image


class ImageUploadView(APIView):
    '''
    post:
    Upload image to server
    '''
    parser_classes = (ImageUploadParser,)
    serializer_class = ImageUploadSerializer

    def post(self, request):
        file: UploadedFile = request.FILES['file']

        with default_storage.open(file.name, 'wb') as f:
            f.write(self.preprocess_image(file))
        url = default_storage.url(file.name)
        serializer = self.serializer_class({'name': file.name, 'url': url})
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def preprocess_image(self, file):
        """Preload image by Pillow and resize before uploading on S3"""
        im = resize_image(file)
        return bytes_from_image(im, settings.IMAGE_FILE_EXTENSION)
