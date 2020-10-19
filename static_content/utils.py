import io

from PIL import Image
from rest_framework.exceptions import ValidationError
from django.conf import settings


def resize_image(file, to_size=settings.DEFAULT_IMAGE_SIZE):
    try:
        img = Image.open(file)
        img.thumbnail(to_size)
        return img
    except IOError as ex:
        raise ValidationError(ex)


def bytes_from_image(image, extension):
    with io.BytesIO() as buff:
        image.save(buff, extension)
        return buff.getvalue()
