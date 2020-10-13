import string
from random import random


def upload_to(_, file_name):
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    file_extension = file_name.split('.')[-1]
    return f'{random_str}.{file_extension}'
