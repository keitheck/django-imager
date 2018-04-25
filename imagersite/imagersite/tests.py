from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class ViewTests(TestCase):
    """test class that tests login view"""
    @classmethod
    def setUp(cls):
        User.objects.create_user(username='testuser', password='SecretPassword')

    def test_login(self):
        """testing that user autheticated correctly after login"""
        # send login data
        response = self.client.post(
            reverse_lazy('auth_login'), 
            {'username': 'testuser', 'password': 'SecretPassword'},
            follow=True,      
            )
        # user should be logged in.
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse_lazy('user_profile'))

    def test_logout(self):
        """testing that user un-autheticated correctly after logout"""
        # send login data
        response = self.client.post(
            reverse_lazy('auth_logout'),     
            )
        # user should be logged out.
        self.assertFalse(response.context['user'].is_authenticated)    

    def test_profile(self):
        """testing that profile path renders successful"""
        response = self.client.get(reverse_lazy('user_profile'))
        self.assertTrue(response.status_code == 200)
        
