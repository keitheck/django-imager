from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from imager_profile.models import ImagerProfile
from model_mommy import mommy
from django.urls import reverse_lazy


class ProfileRouteTest(TestCase):
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

    def test_profile_edit_edits(self):
        """Validate that profile edit view edits instance."""
        profile = ImagerProfile.objects.first()
        profile.bio = 'this is my original bio.'
        profile.save()
        self.client.force_login(profile.user)
        self.client.post(
            reverse_lazy('profile_edit'),
            {
                'bio': 'this is my new profile.',
                'phone': '1234567890',
                'location': 'somewhere',
                'website': 'http://www.somewebsite.com',
                'fee': '5',
                'services': 'weddings',
                'photostyles': 'night',
            })
        self.client.logout()
        profile = ImagerProfile.objects.get(id=profile.id)
        self.assertEqual(profile.bio, 'this is my new profile.')

    def test_profile_edit_redirects_after_edit(self):
        """Validate redirect to library after edit."""
        profile = ImagerProfile.objects.first()
        self.client.force_login(profile.user)
        response = self.client.post(
            reverse_lazy('profile_edit'),
            {
                'bio': 'this is my new profile.',
                'phone': '1234567890',
                'location': 'somewhere',
                'website': 'http://www.somewebsite.com',
                'fee': '5',
                'services': 'weddings',
                'photostyles': 'night',
            },
            follow=True)
        self.client.logout()
        self.assertTemplateUsed(response, 'imager_profile/profile.html')
