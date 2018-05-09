from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from model_mommy import mommy
from django.urls import reverse_lazy


class ProfileRouteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        for _ in range(2):
            mommy.make(User)

    def test_user_views_own_profile(self):
        """Test that user's own profile renders."""
        self.client.force_login(User.objects.first())
        response = self.client.get(reverse_lazy('profile'))
        self.client.logout()
        self.assertTrue(response.status_code == 200)

    def test_user_views_another_profile(self):
        """Test user can render another user's profile."""
        user = User.objects.first()
        user2 = User.objects.exclude(username=user.username).first()
        self.client.force_login(user)
        response = self.client.get(
            reverse_lazy('named_profile', args=[user2.username]))
        self.client.logout()
        self.assertTrue(response.status_code == 200)

    def test_anon_view_profile_redirect(self):
        """Test anon gets redirected when trying to view profiles."""
        response = self.client.get(reverse_lazy(
            'named_profile',
            args=[User.objects.first().username]))

        self.assertTrue(response.status_code == 302)
