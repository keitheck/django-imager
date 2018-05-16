from rest_framework import serializers
from imager_images.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for photo model."""
    class Meta:
        model = Photo
        fields = ('id', 'image.url', 'title', 'description', 'date_uploaded',
                  'date_modified', 'date_published', 'published')
