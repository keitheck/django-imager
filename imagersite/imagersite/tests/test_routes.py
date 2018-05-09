from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse_lazy


class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                username="strider",
                email="strider@aragorn.com",
                password="kingofgondor",)

    def test_anon_gets_homepage(self):
        """Test anonymous user lands on home."""
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_gets_homepage(self):
        """Test authenticated user lands on home."""
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('home'))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_correct_template(self):
        """Test correct content renders."""
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('home'))
        self.client.logout()
        self.assertTemplateUsed(response, 'home.html')
