from django.urls import path
from .views import PhotoListAPIView, UserAPIView
from rest_framework.authtoken import views

urlpatterns = [
        path('photos', PhotoListAPIView.as_view(), name='photo_list_api'),
        path('user', UserAPIView.as_view(), name='user_detail'),
        path('login', views.obtain_auth_token, name='login_api'),
]
