from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from imager_profile.tests.test_models import ProfileFactory


class AuthTests(TestCase):
    """test class that tests login view"""
    @classmethod
    def setUp(cls):
        user = User.objects.create_user(
            username='testuser', password='SecretPassword')
        ProfileFactory.create(user=user)

    def test_login(self):
        """testing that user autheticated correctly after login"""
        # send login data
        response = self.client.post(
             reverse_lazy('auth_login'),
             {'username': 'testuser', 'password': 'SecretPassword'},
             follow=True,
        )
        #  user should be logged in.

        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse_lazy('profile'))

    def test_logout(self):
        """testing that user un-autheticated correctly after logout"""
        # send login data
        response = self.client.post(
            reverse_lazy('auth_logout'),
            )
        # user should be logged out.
        self.assertFalse(response.context['user'].is_authenticated)
