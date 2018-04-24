from django.test import TestCase
from .models import ImagerProfile, User
import factory


class UserFactory(factory.django.DjangoModelFactory):
    '''Factory that creates fake users for testing'''
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')


class ProfileFactory(factory.django.DjangoModelFactory):
    '''Factory that creates fake user profiles for testing'''
    class Meta:
        model = ImagerProfile

    bio = factory.Faker('paragraph')
    phone = factory.Faker('phone_number')
    location = factory.Faker('city')
    website = factory.Faker('url')
    fee = factory.Faker('pydecimal')
    camera = factory.Faker('text', max_nb_chars=100)
    services = factory.Faker('text', max_nb_chars=20)
    is_active = factory.Faker('boolean')


class ProfileUnitTests(TestCase):
    @classmethod
    def setUpClass(cls):
        '''Set up users for testing'''
        super(TestCase, cls)
        for _ in range(5):
            user = UserFactory.create()
            user.set_password(factory.Faker('password'))
            user.save()

            profile = ProfileFactory.create(user=user)
            profile.save()

    @classmethod
    def tearDownClass(cls):
        '''Tear down users after testing'''
        super(TestCase, cls)
        User.objects.all().delete()

    def test_user_can_see_profile(self):
        '''Test user has profile property.'''
        one_user = User.objects.first()
        self.assertIsNotNone(one_user.profile)

    def test_delete_user_deletes_profile(self):
        '''Test profile deleted after user deleted.'''
        one_user = User.objects.first()
        self.assertIsNotNone(ImagerProfile.objects.filter(user=one_user))
        one_user.delete()
        self.assertFalse(ImagerProfile.objects.filter(user=one_user).exists())

    def test_active_filtering(self):
        '''Tests ImagerProfile.active class method'''
        profile = ImagerProfile.objects.first()
        profile.is_active = True
        profile.save()
        self.assertTrue(profile in ImagerProfile.active())
        profile.is_active = False
        profile.save()
        self.assertFalse(profile in ImagerProfile.active())
