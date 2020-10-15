from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.reverse import reverse

from authentication.models import Author, Subscription
from lessons.models import Lesson, Vote
from lessons.serializers import LessonSerializer
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
            'creator': self.user.id,
        }
        self.lesson = Lesson.objects.create(title=self.data['title'],
                                            video_url=self.data['video_url'],
                                            lesson_img=self.data['lesson_img'],
                                            creator_id=self.data['creator'])
        self.serializer = LessonSerializer(self.lesson)

    def logout_and_create_new_user(self):
        self.logout()
        email = 'Csgo1.6@meta.ua'
        password = '@mail.com'
        self.user = self.create_and_authorize(email, password)

    def test_list(self):
        response = self.client.get(reverse('lessons-list'))
        self.assertTrue(response.data)
        self.assertEqual(response.data[0]['title'], self.serializer.data['title'])

    def test_list_user(self):
        response = self.client.get(reverse('lessons-list'), **{'QUERY_STRING': f'creator={self.user.id}'})
        self.assertEqual(response.data[0]['title'], self.data['title'])

    def test_retrieve(self):
        response = self.client.get(reverse('lessons-detail', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.data['title'], self.serializer.data['title'])

    def test_retrieve_not_found(self):
        response = self.client.get(reverse('lessons-detail', kwargs={'pk': self.lesson.id + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create(self):
        response = self.client.post(reverse('lessons-list'), {'title': 'title',
                                                              'video_url': 'video_url',
                                                              'lesson_img': 'test.png'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_validation_error(self):
        response = self.client.post(reverse('lessons-list'), {'taitle': 'title',
                                                              'video_url': 'video_url',
                                                              'lesson_img': 'test.png'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_unauthorized(self):
        self.logout()
        response = self.client.post(reverse('lessons-list'), {'title': 'title',
                                                              'video_url': 'video_url',
                                                              'lesson_img': 'test.png'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update(self):
        update_data = {'title': 'test_update', 'video_url': 'asd'}
        response = self.client.put(reverse('lessons-detail', kwargs={'pk': self.lesson.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], update_data['title'])

    def test_update_not_owner(self):
        self.logout_and_create_new_user()
        update_data = {'title': 'test_update', 'video_url': 'asd'}
        response = self.client.put(reverse('lessons-detail', kwargs={'pk': self.lesson.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.logout()

    def test_update_unauthorized(self):
        self.logout()
        update_data = {'title': 'test_update', 'video_url': 'asd'}
        response = self.client.put(reverse('lessons-detail', kwargs={'pk': self.lesson.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_validation_error(self):
        update_data = {'tiatle': 'test_update', 'videoa_url': 'asd'}
        response = self.client.put(reverse('lessons-detail', kwargs={'pk': self.lesson.id}), update_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        response = self.client.delete(reverse('lessons-detail', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.id).count())

    def test_delete_unauthorized(self):
        self.logout()
        response = self.client.delete(reverse('lessons-detail', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_not_owner(self):
        self.logout_and_create_new_user()
        response = self.client.delete(reverse('lessons-detail', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_toggle_like(self):
        response = self.client.post(reverse('lessons-toggle-like', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Vote.objects.filter(voted=self.user.id).count())

    def test_untoggle_like(self):
        self.client.post(reverse('lessons-toggle-like', kwargs={'pk': self.lesson.id}))
        response = self.client.post(reverse('lessons-toggle-like', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Vote.objects.filter(voted=self.user.id).count())

    def test_subscribe(self):
        self.client.post(reverse('lessons-list'), {'title': 'title',
                                                              'video_url': 'video_url',
                                                              'lesson_img': 'test.png'})
        response = self.client.post(reverse('lessons-subscribe', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(user = self.lesson.creator)
        self.assertTrue(Subscription.objects.filter(author = author, subscriber_id = self.user.id))

    def test_notify_email(self,**additional_headers):
        self.client.post(reverse('lessons-list'), {'title': 'title',
                                                              'video_url': 'video_url',
                                                              'lesson_img': 'test.png'})
        user_creator = self.user
        self.logout_and_create_new_user()
        response = self.client.post(reverse('lessons-subscribe', kwargs={'pk': self.lesson.id}))
        #print(Subscription.objects.filter())
        self.logout()
        self.authorize(user_creator,**additional_headers)
        self.client.post(reverse('lessons-list'), {'title': 'tlitle',
                                                              'video_url': 'vidleo_url',
                                                              'lesson_img': 'test.png'})
