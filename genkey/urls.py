from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_generate_CSR, name='start_generate_CSR'),
    path('configure_CA_subject_name', views.configure_CA_subject_name, name='configure_CA_subject_name'),
    path('configure_CA_key_algorithm', views.configure_CA_key_algorithm, name='configure_CA_key_algorithm'),
    path('configure_certificate_revocation', views.configure_certificate_revocation, name='configure_certificate_revocation'),
    path('review_and_create', views.review_and_create, name='review_and_create'),
    path('request_certificate', views.request_certificate, name='request_certificate'),
    path('export_certificate', views.export_certificate, name='export_certificate'),
    path('CSR_download', views.CSR_download, name='CSR_download'),
    path('certificate_download', views.certificate_download, name='certificate_download'),

]
