from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.views import RegisterApi

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='auth'),
    path('refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('register/', RegisterApi.as_view(), name='auth_register'),
]
