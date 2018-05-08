from imager_images.models import Photo
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Default home route.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ImagerSite Home'
        context['banner'] = Photo.objects.filter(
            published='PUBLIC').order_by('?').first()
        return context
