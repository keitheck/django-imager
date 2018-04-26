from django.shortcuts import render
from imager_images.models import Photo, Album


def home_view(request):
    '''Default "home" route'''
    
    context = {
        'title': 'ImagerSite'
    }

    if Photo.objects.all().count():
        context['banner'] = Photo.objects.order_by('?').first()

    return render(request, 'home.html', context)


# def user_profile_view(request):
#     '''Default landing page after login.'''
#     return render(
#         request, 'user_profile.html', {'title': 'ImagerSite > User Profile'})
