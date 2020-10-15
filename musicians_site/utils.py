import io
import string
import random
from django.conf import settings

from PIL import Image


def generate_random_str(size):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))


def upload_to(_, file_name):
    random_str = generate_random_str(7)
    file_extension = file_name.split('.')[-1]
    return f'{random_str}.{file_extension}'


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGB', size=(100, 100), color=(155, 0, 0))
    image.save(file, settings.IMAGE_FILE_EXTENSION)
    file.name = f'test.{settings.IMAGE_FILE_EXTENSION}'
    file.seek(0)
    return file
