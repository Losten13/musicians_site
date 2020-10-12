from rest_framework.routers import DefaultRouter

from lessons.views import LessonList, VoteView

router = DefaultRouter()
router.register('lessons', LessonList, basename='lessons')
router.register('votes', VoteView, basename='votes')
urlpatterns = router.urls
