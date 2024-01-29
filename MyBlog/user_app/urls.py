from django.urls import path
from user_app import views

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path('reg/', views.reg, name='reg'),
    path('lout/', views.lout, name='lout'),
    path('profile/', views.user_profile, name='user_profile')
]
