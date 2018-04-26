from django.test import TestCase
from .models import Photo, Album, User
from imager_profile.tests import UserFactory
import factory


class PhotoFactory(factory.django.DjangoModelFactory):
    """Factory that creates fake photos for testing"""
    class Meta:
        model = Photo
    title = factory.Faker('text', max_nb_chars=100)
    description = factory.Faker('text')


class AlbumFactory (factory.django.DjangoModelFactory):
    """Factory that creates fake albums for testing"""
    class Meta:
        model = Album
    title = factory.Faker('text', max_nb_chars=100)
    description = factory.Faker('text')


class PhotoAlbumUnitTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCase, cls)
        for _ in range(5):
            user = UserFactory.create()
            # user = User.objects.create(username='testuser')
            user.set_password('CodeFellows')
            user.save()    

            album = AlbumFactory.create(user=user)
            album.save()

            photo = PhotoFactory.create(user=user)
            photo.save()

    @classmethod
    def tearDownClass(cls):
        """tears down test objects"""
        super(TestCase, cls)
        Photo.objects.all().delete()
        Album.objects.all().delete()

    def test_photo_is_created(self):
        """tests if photos were created successfully"""
        self.assertTrue(Photo.objects.count())

    def test_album_is_created(self):
        """tests if album were created successfully"""
        self.assertTrue(Album.objects.count()) 

    def test_album_has_multiple_photos_and_users(self):
        """tests if album takes multiple photos owned by multiple users"""    
        album = Album.objects.first()    
        album.save()
        photo1 = Photo.objects.first()
        photo2 = Photo.objects.all()[1]
        photo1.user = User.objects.first()
        photo2.user = User.objects.all()[1]
        photo1.save()
        photo2.save()
        album.photos.add(photo1, photo2)
        photo_count = album.photos.count()
        self.assertTrue(photo_count == 2)
        self.assertTrue(photo1.user is not photo2.user)

    def test_photo_in_multiple_albums(self):
        """tests if single photo instance can be in multiple albums"""
        album1 = Album.objects.all()[2] 
        album2 = Album.objects.all()[3]
        album1.user = User.objects.all()[2]
        album2.user = User.objects.all()[2]
        photo = Photo.objects.all()[2]
        photo.user = User.objects.all()[2]
        album1.photos.add(photo)
        album2.photos.add(photo)
        album1.save()
        album2.save()
        photo.save()
        self.assertTrue(photo.albums.count() == 2)
    







