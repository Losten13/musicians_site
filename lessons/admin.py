from django.contrib import admin

# Register your models here.
from lessons.models import Lesson, Vote

admin.site.register(Lesson)
admin.site.register(Vote)
