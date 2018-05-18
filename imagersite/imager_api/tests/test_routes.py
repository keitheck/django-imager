from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from model_mommy import mommy
from imager_images.models import Photo
from rest_framework.authtoken.models import Token
import tempfile


class RouteTests(TestCase):
    """Integration tests."""
    def setUp(self):
        self.user = mommy.make(User, password='CodeFellows')
        self.photo = mommy.make(
            Photo,
            user=self.user,
            title='paddington bear',
            image=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        self.token = Token.objects.get(user=self.user).key

    def tearDown(self):
        User.objects.all().delete()
        Photo.objects.all().delete()

    def test_photolist_returns_401_unauthenticated(self):
        """Validate 401 when anonymous."""
        response = self.client.get(reverse_lazy('photo_list_api'))
        self.assertEqual(response.status_code, 401)

    def test_photolist_returns_200_when_auth(self):
        """Validate photolist can be reached."""
        response = self.client.get(
            reverse_lazy('photo_list_api'),
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertEqual(response.status_code, 200)

    def test_photolist_returns_users_photos(self):
        """Validate returned json."""
        response = self.client.get(
            reverse_lazy('photo_list_api'),
            HTTP_AUTHORIZATION=f'Token {self.token}'
        )
        self.assertTrue(len(response.data) == 1)
        self.assertEqual(response.data[0]['title'], 'paddington bear')
