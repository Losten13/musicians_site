from django.db import models

from authentication.models import User


class Lesson(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    video_url = models.CharField(max_length=60)
    votes = models.IntegerField()

