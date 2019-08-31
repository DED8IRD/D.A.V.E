"""screenplay_generator url config
"""
from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'gen'
urlpatterns = [
    re_path('.*', TemplateView.as_view(template_name='index.html'), name='client'),
    path('screenwrite/', views.screenwrite, name='screenwrite'),
]
