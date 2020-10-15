from django.urls import path

from static_content.views import ImageUploadView

urlpatterns = [
    path('image', ImageUploadView.as_view(), name='image')
]
