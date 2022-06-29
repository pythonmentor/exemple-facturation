from django.views.generic import TemplateView
from django.contrib import messages


class HomeView(TemplateView):
    template_name = 'core/home.html'
