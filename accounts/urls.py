
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('', include('django.contrib.auth.urls')),
# path('accounts/signup/', views.signup, name='signup'),
# path('accounts/password_reset/', views.password_reset, name='password_reset'),
    path('', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('register/done/', views.register, name='register_done'),
    path('login/', auth_views.LoginView.as_view(), name='loign'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    ]