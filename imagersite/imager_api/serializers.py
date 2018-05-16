from rest_framework import serializers
from imager_images.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='image.url')

    """Serializer for photo model."""
    class Meta:
        model = Photo
        fields = ('id', 'url', 'title', 'description', 'date_uploaded',
                  'date_modified', 'date_published', 'published')
