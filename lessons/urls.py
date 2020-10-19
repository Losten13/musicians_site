from django.urls import path
from rest_framework.routers import DefaultRouter

from lessons.views import LessonViewSet, UserSubscriberView

router = DefaultRouter()
router.register('lessons', LessonViewSet, basename='lessons')
urlpatterns = router.urls
urlpatterns.append(path('subscribers', UserSubscriberView.as_view(), name='subscribers'))
