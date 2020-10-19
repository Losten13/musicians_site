from rest_framework.parsers import FileUploadParser

from musicians_site.settings import IMAGE_FILE_EXTENSION
from musicians_site.utils import generate_random_str


class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'

    def get_filename(self, stream, media_type, parser_context):
        random_str = generate_random_str(7)
        return f'{random_str}.{IMAGE_FILE_EXTENSION}'
