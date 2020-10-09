from rest_framework.routers import DefaultRouter

from lessons.views import LessonList

router = DefaultRouter()
router.register('lessons', LessonList, basename='lessons')
urlpatterns = router.urls
