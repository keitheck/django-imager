from rest_framework import generics, status
from .serializers import PhotoSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from imager_images.models import Photo


class PhotoListAPIView(generics.ListAPIView):
    """API Endpoint to view user photos."""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = PhotoSerializer

    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)


class UserAPIView(generics.RetrieveAPIView, generics.CreateAPIView):
    """API endpoint to get user metadata or create a user."""
    permission_classes = ''
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        if not pk:
            return Response(UserSerializer(request.user).data,
                            status=status.HTTP_200_OK)
        return super().retrieve(request, pk)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
