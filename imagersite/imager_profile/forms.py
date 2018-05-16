from .models import ImagerProfile
from django.forms import ModelForm


class ProfileEditForm(ModelForm):
    """Instantiate user profile edit forms."""
    class Meta:
        model = ImagerProfile
        fields = [
            'bio',
            'phone',
            'location',
            'website',
            'fee',
            'camera',
            'services',
            'photostyles']

        def __init__(self, *args, **kwargs)::
        username = kwargs.pop('username')
        super().__init__(*args, **kwargs)
        user = ImagerProfile.objects.get(user__username=username)
        self.fields['bio'].initial = user.bio
        self.fields['phone'].initial = user.phone
        self.fields['location'].initial = user.location
        self.fields['website'].initial = user.bio
        self.fields['fee'].initial = user.phone
        self.fields['camera'].initial = user.phone
        self.fields['services'].initial = user.bio
        self.fields['photostyles'].initial = user.phone
