from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('decoder/', views.decoder, name='decoder'),
    path('create/', views.create, name='create'),
    path('decoder/info', views.decoder_info, name='decoder_info'),
    ]