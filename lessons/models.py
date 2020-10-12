from django.db import models

from authentication.models import User


class Lesson(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    video_url = models.CharField(max_length=60)
    lesson_img = models.ImageField(upload_to='lesson/', blank=True, default=None)
    # todo imagefield


class Vote(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='votes', on_delete=models.CASCADE)
    voted = models.ForeignKey(User, on_delete=models.CASCADE)
    is_voted = models.BooleanField(default=True)


