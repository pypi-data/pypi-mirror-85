from django.views.generic.base import TemplateView
from django.shortcuts import render

class IndexView(TemplateView):
    template_name = 'home/index.html'

class AboutView(TemplateView):
    template_name = 'home/about.html'

class ContactView(TemplateView):
    template_name = 'home/contact.html'