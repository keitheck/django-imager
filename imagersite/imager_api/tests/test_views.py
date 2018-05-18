from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
import tempfile
from imager_images.models import Photo
from ..views import PhotoListAPIView, UserAPIView


class TestAPIViews(TestCase):
    """Tests for API Views."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
                username='peregrin',
                email='crazytook@hotmail.com',
        )
        self.user1.password = 'greybeardforever'
        self.user1.save()
        self.user2 = User.objects.create_user(
                username='meriadoc',
                email='kneebiter@kingslayers.net',
        )
        self.user2.password = '10v1Nth35h1r3'
        self.user2.save()
        self.photo1 = Photo.objects.create(
                user=self.user1,
                image=tempfile.NamedTemporaryFile(suffix='.jpg').name,
                title='The Enting',
                description='A picture of ents gathering.',
                published='PRIVATE',
        )
        self.photo2 = Photo.objects.create(
                user=self.user2,
                image=tempfile.NamedTemporaryFile(suffix='.jpg').name,
                title='Sword beats Nazgul',
                description='Eowyn being a boss.',
                published='PUBLIC',
        )

    def tearDown(self):
        User.objects.all().delete()
        Photo.objects.all().delete()

    def test_photolist_returns_401_unauthenticated(self):
        """Validate 401 when anonymous."""
        request = self.factory.get('api/v1/photos')
        request.user = AnonymousUser
        response = PhotoListAPIView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_photolist_returns_200_when_auth(self):
        """Validate photolist can be reached."""
        token = Token.objects.get(user=self.user1).key
        request = self.factory.get(
            reverse_lazy('photo_list_api'),
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        request.user = self.user1
        response = PhotoListAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_photolist_returns_users_photos(self):
        """Validate returned json."""
        token = Token.objects.get(user=self.user1).key
        request = self.factory.get(
            reverse_lazy('photo_list_api'),
            HTTP_AUTHORIZATION=f'Token {token}'
        )
        request.user = self.user1
        response = PhotoListAPIView.as_view()(request)
        self.assertTrue(len(response.data) == 1)
        self.assertEqual(response.data[0]['title'], 'The Enting')
