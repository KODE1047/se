# /django_pwa/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Connect our app
    path('', include('pwa.urls')),   # Connect PWA features
]
