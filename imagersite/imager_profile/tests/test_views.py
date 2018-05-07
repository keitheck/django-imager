from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from ..views import profile_view
from model_mommy import mommy
from django.urls import reverse_lazy
from django.http import Http404


class ProfileViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        for _ in range(2):
            mommy.make(User)

    def test_user_views_own_profile(self):
        """Test that user's own profile renders."""
        request = self.factory.get(reverse_lazy('profile'))
        request.user = User.objects.first()
        response = profile_view(request)

        self.assertTrue(response.status_code == 200)

    def test_user_views_another_profile(self):
        """Test user can render another user's profile."""
        user = User.objects.first()
        request = self.factory.get(reverse_lazy('named_profile', args=[
            User.objects.exclude(username=user.username).first().username]))
        request.user = User.objects.first()
        response = profile_view(request)

        self.assertTrue(response.status_code == 200)

    def test_anon_view_profile_redirect(self):
        """Test anon gets redirected when trying to view profiles."""
        request = self.factory.get(reverse_lazy('named_profile', args=[
            User.objects.first().username]))
        request.user = AnonymousUser()
        response = profile_view(request)

        self.assertTrue(response.status_code == 302)
