from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from imager_images.models import Photo
from ..views import home_view
from django.urls import reverse_lazy
from model_mommy import mommy
import tempfile


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                username="strider",
                email="strider@aragorn.com",
                password="kingofgondor",)

    def test_anon_gets_homepage(self):
        """Test anonymous user lands on home."""
        request = self.factory.get(reverse_lazy('home'))
        request.user = AnonymousUser()
        response = home_view(request)

        self.assertEqual(response.status_code, 200)

    def test_authenticated_gets_homepage(self):
        """Test authenticated user lands on home."""
        request = self.factory.get(reverse_lazy('home'))
        request.user = self.user
        response = home_view(request)

        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        """Tests correct template renders."""
        request = self.factory.get(reverse_lazy('home'))
        response = home_view(request)

        self.assertContains(response, 'ImagerSite Home')

    def test_banner(self):
        """Tests a banner gets rendered when a public photo exists."""
        photo = mommy.make(
            Photo,
            published='PUBLIC',
            image=tempfile.NamedTemporaryFile(suffix='.jpg').name)
        request = self.factory.get(reverse_lazy('home'))
        response = home_view(request)

        self.assertContains(response, photo.image.url)
