from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start, name='start'),
    path('decoder/', views.decoder, name='decoder'),
    path('create/', views.create, name='create'),
    path('decoder/info', views.decoder_info, name='decoder_info'),
    path('countries_in_JSON/', views.countries_in_JSON, name='countries_in_JSON'),
    path('retrive_CSR_table_data/', views.retrive_CSR_table_data , name='retrive_CSR_table_data'),
    path('create/downlaod_csr', views.downlaod_csr, name='downlaod_csr'),

    ]