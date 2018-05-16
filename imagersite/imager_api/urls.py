from django.urls import path
from .views import PhotoListAPIView


urlpatterns = [
        path('photos', PhotoListAPIView.as_view(), 'photo_list_api')
]
