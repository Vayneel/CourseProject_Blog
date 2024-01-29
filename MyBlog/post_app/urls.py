from django.urls import path
from post_app import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('read/<post_url>/', views.read_post, name='read_post'),
    path('search/', views.search_post, name='search_post'),
    path('favorites/', views.favorites, name='favorites')
]
