from django.shortcuts import render, redirect, get_object_or_404
from .models import ImagerProfile
from imager_images.models import Photo, Album

def profile_view(request, username=None):
    owner = False

    if not username:
        username = request.user.get_username()
        # owner = True
        if username == '':
            return redirect('auth_login')

    profile = get_object_or_404(ImagerProfile, user__username=username)



def library_view():
    pass


        


