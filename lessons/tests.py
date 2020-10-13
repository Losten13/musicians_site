from django.test import TestCase

# Create your tests here.
from rest_framework.reverse import reverse

from lessons.models import Lesson
from musicians_site.tests import APITestUser


class TestLessonViewSet(APITestUser):

    def setUp(self) -> None:
        self.email = 'a@a.com'
        self.password = '123qwe123'
        self.user = self.create_and_authorize(self.email, self.password)
        self.data = {
            'title': 'title',
            'video_url': 'video_url',
            'lesson_img': 'test.png',
            'creator_id': self.user.id,
        }
        self.lesson = Lesson.objects.create(title=self.data['title'],
                                            video_url=self.data['video_url'],
                                            lesson_img=self.data['lesson_img'],
                                            creator_id=self.data['creator_id'])

    def test_list(self):
        response = self.client.get(reverse('lessons-list'))
        self.assertTrue(response.data)
        self.assertEqual(response.data[0]['title'], self.data['title'])

    def test_list_user(self):
        pass

    def test_retrieve(self):
        response = self.client.get(reverse('lessons-retrieve'), kwargs={'pk': self.lesson.id})

    def test_retrieve_not_found(self):
        pass

    def test_create(self):
        pass

    def test_create_validation_error(self):
        pass

    def test_create_unauthorized(self):
        pass

    def test_update(self):
        pass

    def test_update_not_owner(self):
        pass

    def test_update_unauthorized(self):
        pass

    def test_update_validation_error(self):
        pass

    def test_delete(self):
        pass

    def test_delete_unauthorized(self):
        pass

    def test_delete_not_owner(self):
        pass

    def test_toggle_like(self):
        pass

    def test_untoggle_like(self):
        pass

        # TODO: test get list lessons
        # TODO: test get detail lesson
        # TODO: test post lesson: in response, in DB
        # TODO: test post lesson validation error
        # TODO: test put/patch lesson: in response, in DB
        # TODO: test put lesson validation error
        # TODO: test delete lesson
        # TODO: test get when logout
