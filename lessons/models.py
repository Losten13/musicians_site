from django.db import models

from authentication.models import User
from musicians_site.utils import upload_to


class LessonManager(models.Manager):
    def create_lesson(self, title, video_url, creator, *args, **kwargs):
        lesson = self.model(title=title, video_url=video_url, creator=creator, **kwargs)
        lesson.save()
        return lesson


class Lesson(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    video_url = models.CharField(max_length=60)
    lesson_img = models.ImageField(upload_to=upload_to, blank=True, default=None)

    objects = LessonManager()

    class Meta:
        db_table = 'lessons'
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'


class Vote(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='votes', on_delete=models.CASCADE)
    voted = models.ForeignKey(User, on_delete=models.CASCADE)     

    class Meta:
        db_table = 'votes'
        verbose_name = 'vote'
        verbose_name_plural = 'votes'


