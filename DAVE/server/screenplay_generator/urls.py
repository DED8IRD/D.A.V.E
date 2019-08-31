"""screenplay_generator url config
"""
from django.urls import re_path
from django.views.generic import TemplateView

app_name = 'gen'
urlpatterns = [
    re_path('.*', TemplateView.as_view(template_name='index.html'), name='client'),
]
