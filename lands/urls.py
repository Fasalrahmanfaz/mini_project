from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lands/', views.land_list, name='land_list'),
    path('land/<slug:slug>/', views.land_detail, name='land_detail'),
    path('add-land/', views.add_land, name='add_land'),
    path('land/<slug:slug>/edit/', views.edit_land, name='edit_land'),
    path('land/<slug:slug>/delete/', views.delete_land, name='delete_land'),
    path('land/<slug:slug>/inquiry/', views.inquiry, name='inquiry'),
    path('land/<slug:slug>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('my-favorites/', views.my_favorites, name='my_favorites'),
    path('my-inquiries/', views.my_inquiries, name='my_inquiries'),
]