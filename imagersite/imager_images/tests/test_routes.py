from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from ..models import Album, Photo
from model_mommy import mommy
import tempfile


class RouteTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up some users, albums and photos."""
        super(TestCase, cls)
        for _ in range(5):
            user = mommy.make(User, password='CodeFellows')
            photo = mommy.make(Photo, user=user)
            mommy.make(Album, user=user, cover=photo)

    @classmethod
    def tearDownClass(cls):
        """tears down test objects"""
        super(TestCase, cls)
        Photo.objects.all().delete()
        Album.objects.all().delete()
        User.objects.all().delete()

    def test_library_view_redirect(self):
        """Validate library view redirects without login."""
        response = self.client.get(reverse('library'))
        self.assertEqual(response.status_code, 302)

    def test_library_view_logged_in(self):
        """Validate library view shows when logged in."""
        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('library'))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_library_view_renders_library_template(self):
        """Validate correct template is used."""
        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('library'))
        self.client.logout()
        self.assertTemplateUsed(response, 'imager_images/library.html')

    def test_photo_gallery_view_anonymous(self):
        """Validate photo_gallery view shows with anon."""
        response = self.client.get(reverse('photo_gallery'))
        self.assertEqual(response.status_code, 200)

    def test_viewing_photo_gallery_logged_in(self):
        """Validate logged in user sees photo_gallery."""
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('library'))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_photo_gallery_view_renders_photo_gallery_template(self):
        """Validate correct template is used."""
        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('photo_gallery'))
        self.client.logout()
        self.assertTemplateUsed(response, 'imager_images/photo_gallery.html')

    def test_album_gallery_view_anonymous(self):
        """Validate album_gallery view shows with anon."""
        response = self.client.get(reverse('album_gallery'))
        self.assertEqual(response.status_code, 200)

    def test_album_gallery_view_logged_in(self):
        """Validate album_gallery view shows with logged in user."""
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse('album_gallery'))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_album_gallery_view_renders_album_gallery_template(self):
        """Validate correct template is used."""
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('album_gallery'))
        self.client.logout()
        self.assertTemplateUsed(response, 'imager_images/album_gallery.html')

    def test_album_view(self):
        """Validate album view exists."""
        album = Album.objects.all().first()
        album.user = User.objects.all().first()
        album.published = 'PUBLIC'
        album.save()
        response = self.client.get(reverse_lazy('album', args=[album.id]))
        self.assertEqual(response.status_code, 200)

    def test_private_album_renders_404(self):
        """Validate private album doesn't show for anon."""
        album = Album.objects.first()
        album.user = User.objects.first()
        album.published = 'PRIVATE'
        album.save()
        response = self.client.get(reverse_lazy('album', args=[album.id]))
        self.assertEqual(response.status_code, 404)

    def test_album_view_template(self):
        """Validate album view renders correct template."""
        album = Album.objects.all().first()
        album.user = User.objects.all().first()
        album.published = 'PUBLIC'
        album.save()
        response = self.client.get(reverse_lazy('album', args=[album.id]))
        self.assertTemplateUsed(response, 'imager_images/album.html')

    def test_photo_view(self):
        """Validate photo view exists and renders."""
        photo = Photo.objects.all().first()
        photo.user = User.objects.all().first()
        photo.published = 'PUBLIC'
        photo.save()
        response = self.client.get(reverse('photo', args=[photo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'imager_images/photo.html')

    def test_private_photo_renders_404(self):
        """Validate private photo doesn't show for anon."""
        photo = Photo.objects.first()
        photo.user = User.objects.first()
        photo.published = 'PRIVATE'
        photo.save()
        response = self.client.get(reverse_lazy('photo', args=[photo.id]))
        self.assertEqual(response.status_code, 404)

    def test_photo_view_template(self):
        """Validate photo view renders correct template."""
        photo = Photo.objects.all().first()
        photo.user = User.objects.all().first()
        photo.published = 'PUBLIC'
        photo.save()
        response = self.client.get(reverse('photo', args=[photo.id]))
        self.assertTemplateUsed(response, 'imager_images/photo.html')

    def test_album_add_view_exists(self):
        """Validate album add view exists for logged-in user."""
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse('album_add'))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_photo_add_view_exists(self):
        """Validate photo add view exists for logged-in user."""
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse('photo_add'))
        self.client.logout()
        self.assertEqual(response.status_code, 200)

    def test_album_add_redirects_if_not_logged_in(self):
        """Validate can't access view if anon."""
        response = self.client.get(reverse('album_add'))
        self.assertEqual(response.status_code, 302)

    def test_photo_add_redirects_if_not_logged_in(self):
        """Validate can't access view if anon."""
        response = self.client.get(reverse('photo_add'))
        self.assertEqual(response.status_code, 302)

