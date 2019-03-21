from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('configure_CA_subject_name', views.configure_CA_subject_name, name='configure_CA_subject_name'),
    path('configure_CA_key_algorithm', views.configure_CA_key_algorithm, name='configure_CA_key_algorithm'),
    ]
