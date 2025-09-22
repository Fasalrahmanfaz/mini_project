# File: C:\Users\91999\Desktop\Fasal Documents\landmarket\landmarket\urls.py

"""
URL configuration for landmarket project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from lands import views as lands_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lands.urls')),
    path('accounts/', include('accounts.urls')),
    path('about/', lands_views.about, name='about'),  # Added about page
    path('contact/', lands_views.contact, name='contact'),  # Added contact page
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)