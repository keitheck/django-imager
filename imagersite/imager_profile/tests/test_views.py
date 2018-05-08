from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from ..views import ProfileView
from ..models import ImagerProfile
from model_mommy import mommy
from django.urls import reverse_lazy
from django.http import Http404


class ProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        for _ in range(2):
            user = mommy.make(User)
            mommy.make(ImagerProfile, user=user)

    def test_user_views_own_profile(self):
        """Test that user's own profile renders."""
        request = self.factory.get(reverse_lazy('profile'))
        request.user = User.objects.first()
        response = ProfileView.as_view()(request)

        self.assertTrue(response.status_code == 200)

    def test_user_views_another_profile(self):
        """Test user can render another user's profile."""
        user = User.objects.first()
        request = self.factory.get(reverse_lazy('named_profile', args=[
            User.objects.exclude(username=user.username).first().username]))
        request.user = User.objects.first()
        response = ProfileView.as_view()(request)

        self.assertTrue(response.status_code == 200)

    def test_anon_view_profile_redirect(self):
        """Test anon gets redirected when trying to view profiles."""
        request = self.factory.get(reverse_lazy('named_profile', args=[
            User.objects.first().username]))
        request.user = AnonymousUser()
        response = ProfileView.as_view()(request)

        self.assertTrue(response.status_code == 302)

    def test_invalid_profile_raises_404(self):
        """Test accessing a user with no profile raises a 404."""
        user = mommy.make(User)
        request = self.factory.get(reverse_lazy('named_profile', args=[
            User.objects.filter(username=user.username).first().username]))
        request.user = user

        with self.assertRaises(Http404):
            ProfileView.as_view()(request)
