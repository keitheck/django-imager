from django.shortcuts import render


def home_view(request):
    '''Default "home" route'''
    return render(request, 'home.html')


def user_profile_view(request):
    '''Default landing page after login.'''
    return render(request, 'user_profile.html')
