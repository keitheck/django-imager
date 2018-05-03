from django.shortcuts import render
from imager_images.models import Photo


def home_view(request):
    '''Default "home" route'''

    context = {
        'title': 'ImagerSite Home'
    }

    if Photo.objects.all().count():
        context['banner'] = Photo.objects.filter(
            published='PUBLIC').order_by('?').first()

    return render(request, 'home.html', context)
