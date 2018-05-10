from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import render
from ..views import (
    LibraryView,
    PhotoView,
    AlbumView,
    AlbumAddView,
    PhotoAddView,
    PhotoGalleryView,
    AlbumGalleryView)
from ..models import Album, Photo
from model_mommy import mommy
import tempfile


class ViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up some users, albums and photos."""
        super(TestCase, cls)
        for _ in range(5):
            user = mommy.make(User, password='CodeFellows')
            photo = mommy.make(
                Photo,
                user=user,
                image=tempfile.NamedTemporaryFile(suffix='.jpg').name)
            mommy.make(Album, user=user, cover=photo)

    @classmethod
    def tearDownClass(cls):
        """tears down test objects"""
        super(TestCase, cls)
        Photo.objects.all().delete()
        Album.objects.all().delete()

    def test_PhotoView(self):
        """Validate photo view exists and renders."""
        photo = Photo.objects.all().first()
        photo.user = User.objects.all().first()
        photo.published = 'PUBLIC'
        request = RequestFactory().get(reverse_lazy('photo', args=[photo.id]))
        request.user = photo.user
        response = PhotoView.as_view()(request, photo_id=photo.id)
        self.assertEqual(response.status_code, 200)

    def test_photo_view_public_contents(self):
        """Validate view returns photo template."""
        user = User.objects.first()
        photo = Photo.objects.first()
        request = RequestFactory().get(reverse_lazy('photo', args=[photo.id]))
        request.user = user
        photo.published = 'PUBLIC'
        response = PhotoView.as_view()(request, photo_id=photo.id)
        self.assertContains(response, photo.image.url)

    def test_non_public_photo_raises_404(self):
        """Validate a non-public photo raises a 404."""
        user = User.objects.first()
        photo = Photo.objects.exclude(user=user).first()
        photo.published = 'PRIVATE'
        photo.save()
        request = RequestFactory().get(reverse_lazy('photo', args=[photo.id]))
        request.user = user
        with self.assertRaises(Http404):
            PhotoView.as_view()(request, photo_id=photo.id)

    def test_album_view_public(self):
        """Validate view returns 200 status code."""
        user = User.objects.first()
        album = Album.objects.first()
        request = RequestFactory().get(reverse_lazy('album', args=[album.id]))
        request.user = user
        album.published = 'PUBLIC'
        response = AlbumView.as_view()(request, album_id=album.id)
        self.assertEqual(response.status_code, 200)

    def test_non_public_album_raises_404(self):
        """Validate a non-public album raises a 404."""
        user = User.objects.first()
        album = Album.objects.exclude(user=user).first()
        album.published = 'PRIVATE'
        album.save()
        request = RequestFactory().get(reverse_lazy('album', args=[album.id]))
        request.user = user
        with self.assertRaises(Http404):
            AlbumView.as_view()(request, album_id=album.id)

    def test_album_view_public_contents(self):
        """Validate view returns album contents."""
        user = User.objects.first()
        album = Album.objects.first()
        request = RequestFactory().get(reverse_lazy('album', args=[album.id]))
        request.user = user
        album.published = 'PUBLIC'
        response = AlbumView.as_view()(request, album_id=album.id)
        self.assertContains(response, album.title)

    def test_photo_gallery_view_status(self):
        """Validate 200 viewing photo gallery."""
        request = RequestFactory().get(reverse_lazy('photo_gallery'))
        response = PhotoGalleryView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_photo_gallery_view_has_no_private(self):
        """Validate photo gallery shows no private photos."""
        for photo in Photo.objects.all():
            photo.published = 'PRIVATE'
            photo.save()
        request = RequestFactory().get(reverse_lazy('photo_gallery'))
        response = PhotoGalleryView.as_view()(request).render()
        for photo in Photo.objects.all():
            self.assertNotIn(photo.title, response.content.decode('utf-8'))

    def test_photo_gallery_view_has_public(self):
        """Validate photo gallery shows all public photos."""
        photo = Photo.objects.first()
        photo.published = 'PUBLIC'
        photo.save()
        request = RequestFactory().get(reverse_lazy('photo_gallery'))
        response = PhotoGalleryView.as_view()(request).render()
        self.assertIn(photo.title, response.content.decode('utf-8'))

    def test_album_gallery_view_status(self):
        """Validate 200 viewing album gallery."""
        request = RequestFactory().get(reverse_lazy('album_gallery'))
        response = AlbumGalleryView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_album_gallery_view_has_no_private(self):
        """Validate album gallery shows no private albums."""
        for album in Album.objects.all():
            album.published = 'PRIVATE'
            album.save()
        request = RequestFactory().get(reverse_lazy('album_gallery'))
        request.user = User.objects.first()
        response = AlbumGalleryView.as_view()(request).render()
        for album in Album.objects.all():
            self.assertNotIn(album.title, response.content.decode('utf-8'))

    def test_album_gallery_view_has_public(self):
        """Validate album gallery shows all public albums."""
        album = Album.objects.all().first()
        album.published = 'PUBLIC'
        album.save()
        request = RequestFactory().get(reverse_lazy('album_gallery'))
        response = AlbumGalleryView.as_view()(request).render()
        self.assertIn(album.title, response.content.decode('utf-8'))

    def test_library_view_user(self):
        """Validate library view exists and is rendered with user"""
        user = User.objects.all().first()
        self.client.login(username=user.username, password=user.password)
        request = RequestFactory().get(reverse('library'))
        request.user = user
        response = LibraryView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_library_view_renders_library_template(self):
        """Validate correct template is used."""
        user = User.objects.all().first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy('library'))
        self.assertTemplateUsed(response, 'imager_images/library.html')
        self.client.logout()

    def test_album_add_view_exists(self):
        """Validate album add view exists for logged-in user."""
        user = User.objects.first()
        request = RequestFactory().get(reverse('album_add'))
        request.user = user
        response = AlbumAddView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_photo_add_view_exists(self):
        """Validate photo add view exists for logged-in user."""
        user = User.objects.first()
        request = RequestFactory().get(reverse('photo_add'))
        request.user = user
        response = PhotoAddView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_album_add_redirects_if_not_logged_in(self):
        """Validate can't access view if anon."""
        request = RequestFactory().get(reverse('album_add'))
        request.user = AnonymousUser()
        response = AlbumAddView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_photo_add_redirects_if_not_logged_in(self):
        """Validate can't access view if anon."""
        request = RequestFactory().get(reverse('photo_add'))
        request.user = AnonymousUser()
        response = PhotoAddView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_library_view_redirect_anon(self):
        """Validate library view redirects when anon."""
        request = RequestFactory().get(reverse('library'))
        request.user = AnonymousUser()
        response = LibraryView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_library_shows_user_albums(self):
        """Validate library shows private user album."""
        user = User.objects.first()
        album = Album.objects.first()
        album.user = user
        request = RequestFactory().get(reverse('library'))
        request.user = user
        response = LibraryView.as_view()(request)
        self.assertContains(response, album.title)

   # def test_photo_add_adds(self):
   #     request = RequestFactory().post(reverse('photo_add'), {'image': tempfile.NamedTemporaryFile(suffix='.jpg').name, 'title': 'Untitled', 'description': 'Description', 'published': 'PUBLIC'})
   #     response = LibraryView.as_view()(request)
   #     self.assertEqual(response.status_code, 302)
