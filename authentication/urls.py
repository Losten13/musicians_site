from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import RegisterView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('register/', RegisterView.as_view(), name='auth-register'),
]
