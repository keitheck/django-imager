from rest_framework import generics
from .serializers import PhotoSerializer
from imager_images.models import Photo


class PhotoListAPIView(generics.ListAPIView):
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)
