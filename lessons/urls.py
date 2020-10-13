from rest_framework.routers import DefaultRouter

from lessons.views import LessonViewSet, VoteViewSet

router = DefaultRouter()
router.register('lessons', LessonViewSet, basename='lessons')
router.register('votes', VoteViewSet, basename='votes')
urlpatterns = router.urls
