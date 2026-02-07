# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # API Versioning v1
    path('api/v1/', include('config.api_router')), 
]