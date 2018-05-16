from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from ..views import ProfileView, ProfileEditView
from ..models import ImagerProfile
from model_mommy import mommy
from django.urls import reverse_lazy


class ProfileViewTest(TestCase):
    def setUp(self):
        """Set up test users and profiles."""
        self.factory = RequestFactory()
        for _ in range(2):
            mommy.make(User)

    def tearDown(self):
        """Tear down test users and profiles."""
        User.objects.all().delete()

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

    def test_profile_edit_exists(self):
        """Validate profile edit view renders for owner of profile."""
        user = User.objects.first()
        request = RequestFactory().get(reverse_lazy('profile_edit'))
        request.user = user
        response = ProfileEditView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_prepopulates(self):
        """Validate that the current profile data displays in the form."""
        user = User.objects.first()
        profile = ImagerProfile.objects.get(user=user)
        profile.bio = 'I am a profile bio.'
        profile.save()
        request = RequestFactory().get(reverse_lazy('profile_edit'))
        request.user = user
        response = ProfileEditView.as_view()(request)
        self.assertContains(response, profile.bio)

    def test_profile_edit_redirect_if_not_logged_in(self):
        """Validate that anon cannot access edit view."""
        user = AnonymousUser()
        request = RequestFactory().get(reverse_lazy('profile_edit'))
        request.user = user
        response = ProfileEditView.as_view()(request)
        self.assertEqual(response.status_code, 302)
