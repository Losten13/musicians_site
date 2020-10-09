from django.test import TestCase

# Create your tests here.
from authentication.tests import APITestUser


class TestLessonViewSet(APITestUser):

    def setUp(self) -> None:
        self.user = self.create_and_authorize()

        # TODO: test get list lessons
        # TODO: test get detail lesson
        # TODO: test post lesson: in response, in DB
        # TODO: test post lesson validation error
        # TODO: test put/patch lesson: in response, in DB
        # TODO: test put lesson validation error
        # TODO: test delete lesson
        # TODO: test get when logout
