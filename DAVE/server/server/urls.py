"""server URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('screenplay_generator.urls')),
    path('admin/', admin.site.urls),
]
