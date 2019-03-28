import sys, pycurl,json, random, hashlib, calendar,time, datetime, os, random

from django.shortcuts import render
from .forms import subjectForm, algorithmForm, CRLForm, CA_choice
from django.shortcuts import redirect
from django.http import Http404
import json
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption,load_pem_private_key
from .models import Issuer
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.x509 import load_pem_x509_csr
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend
from django.conf import settings
from django.http import HttpResponse, Http404
from .models import Company
# Create your views here.
def start_generate_CSR(request):
    return render(request, 'genkey/start_generate_CSR.html', {})

def configure_CA_subject_name(request):
    form = subjectForm()
    return render(request, 'genkey/configure_CA_subject_name.html', {'form': form})


def configure_CA_key_algorithm(request):
    print(request.POST)
    prev_form = subjectForm(request.POST)
    if prev_form.is_valid():

        organization = prev_form.cleaned_data['organization']
        organization_unit = prev_form.cleaned_data['organization_unit']
        country = prev_form.cleaned_data['country']
        state = prev_form.cleaned_data['state']
        locality = prev_form.cleaned_data['locality']
        common_name = prev_form.cleaned_data['common_name']
        domain = prev_form.cleaned_data['domain']
    form = algorithmForm()
    return render(request, 'genkey/configure_CA_key_algorithm.html', {'form':form, 'organization':organization, 'organization_unit':organization_unit,
                  'country':country, 'state':state, 'locality':locality , 'common_name':common_name, 'domain':domain})

def configure_certificate_revocation(request):
    print(request.POST)
    prev_form = algorithmForm(request.POST)
    if prev_form.is_valid():
        algorithm = prev_form.cleaned_data['algorithm']

    organization = request.POST['organization']
    organization_unit = request.POST['organization_unit']
    country = request.POST['country']
    state = request.POST['state']
    locality = request.POST['locality']
    common_name = request.POST['common_name']

    form = CRLForm()
    return render(request, 'genkey/configure_certificate_revocation.html', {'form': form, 'algorithm':algorithm,'organization':organization, 'organization_unit':organization_unit,
                  'country':country, 'state':state, 'locality':locality , 'common_name':common_name } )

def review_and_create(request):
    print(request.POST)
    prev_form = algorithmForm(request.POST)
    if prev_form.is_valid():
        algorithm = prev_form.cleaned_data['algorithm']

    organization = request.POST['organization']
    algorithm = request.POST['algorithm']
    organization_unit = request.POST['organization_unit']
    country = request.POST['country']
    state = request.POST['state']
    locality = request.POST['locality']
    common_name = request.POST['common_name']
    domain = request.POST['domain']

    ca = Company()
    ca.algorithm = algorithm
    ca.organization = organization
    ca.organization_unit = organization_unit
    ca.country = country
    ca.state = state
    ca.locality = locality
    ca.common_name = common_name
    ca.domain = domain

    if algorithm == "rsa_2048":
        ca_private_key = generate_RSA_private_key(2048)
        print(ca.private_key)
    elif algorithm == "rsa_4096":
        ca_private_key = generate_RSA_private_key(4096)
        print(ca.private_key)

    elif algorithm == "ecdsa_p256":
        ca_private_key = generate_ECP256_private_key()
        print(ca.private_key)

    elif algorithm == "ecdsa_p384":
        ca_private_key = generate_ECP384_private_key()
        print(ca.private_key)



    csr = x509.CertificateSigningRequestBuilder().subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])).add_extension(
        x509.SubjectAlternativeName([
            # Describe what sites we want this certificate for.
            x509.DNSName(domain),
        ]),
        critical=False,
        # Sign the CSR with our private key.
    ).sign(ca_private_key, hashes.SHA256(), default_backend())


    ca.private_key = encode_private_key_pem_format(ca_private_key)
    CA_public_key = generate_pub_key(ca_private_key)
    ca.public_key = encode_public_key_pem_format(CA_public_key)
    ca.save()
    csr = csr.public_bytes(serialization.Encoding.PEM).decode()
    return render(request, 'genkey/review_and_create.html', {'csr':csr})

def request_certificate(request):
    form = CA_choice(request.POST)
    csr = request.POST['csr']
    return render(request, 'genkey/request_certificate.html', {'form':form, 'csr':csr})

def export_certificate(request):
    issuer_pk = request.POST['CA']
    issuer_a = Issuer.objects.get(pk=int(issuer_pk))
    subject = Company.objects.all()[0]

    # with open("./private_key.pem", "rb") as f:
    #     private_key_pem = f.read()
    #     CA_private_key = load_pem_private_key(private_key_pem, password=None, backend=default_backend())
    # with open("./public_key.pem", "rb") as f:
    #     public_key_pem = f.read()
    #     CA_public_key = serialization.load_pem_public_key(
    #     public_key_pem,
    #     backend=default_backend()
    #     )
    #
    # issuer.private_key = subject.private_key
    # issuer.public_key = subject.public_key
    # issuer.save()
    # subsub = load_pem_private_key(issuer.private_key.encode(), password=None, backend=default_backend())
    # print(subsub)
    # CA_public_key = serialization.load_pem_public_key(
    #     issuer.public_key.encode(),
    #     backend=default_backend()
    # )
    # print(CA_public_key)




    CA_private_key =  load_pem_private_key(issuer_a.private_key.encode(), password=None, backend=default_backend())
    CA_public_key = serialization.load_pem_public_key(
        issuer_a.public_key.encode(),
        backend=default_backend()
    )
    #CA_private_key = decode_private_key_byte_format(issuer.private_key)
    #CA_public_key = decode_public_key_byte_format(issuer.public_key)
    csr = load_pem_x509_csr(request.POST['csr'].encode(), backend=default_backend())
    print(issuer_a.domain)
    subject_country = csr.subject.get_attributes_for_oid(NameOID.COUNTRY_NAME)[0].value.capitalize()
    subject_common_name = csr.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value
    subject_organization = csr.subject.get_attributes_for_oid(NameOID.ORGANIZATION_NAME)[0].value
    subject_locality = csr.subject.get_attributes_for_oid(NameOID.LOCALITY_NAME)[0].value
    subject_state = csr.subject.get_attributes_for_oid(NameOID.STATE_OR_PROVINCE_NAME)[0].value

    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, subject_country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, subject_state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, subject_locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject_organization),
        x509.NameAttribute(NameOID.COMMON_NAME, subject_common_name),
    ])

    issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, issuer_a.country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, issuer_a.state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, issuer_a.locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, issuer_a.organization),
        x509.NameAttribute(NameOID.COMMON_NAME, issuer_a.common_name),
    ])


    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        CA_public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Our certificate will be valid for 10 days
        datetime.datetime.utcnow() + datetime.timedelta(days=3650)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(issuer_a.domain)]),
        critical=False,
        # Sign our certificate with our private key
    ).sign(CA_private_key, hashes.SHA256(), default_backend())
    # Write our certificate out to disk.

    certificate = cert.public_bytes(
                encoding=serialization.Encoding.PEM,
            ).decode()


    return render(request, 'genkey/export_certificate.html', {'certificate':certificate, 'certificate':certificate})






def generate_RSA_private_key(KEY_SIZE):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=KEY_SIZE,
        backend=default_backend()
    )
    return private_key

def generate_ECP384_private_key():
    private_key = ec.generate_private_key(
    ec.SECP384R1(), default_backend()
    )
    return private_key

def generate_ECP256_private_key():
    private_key = ec.generate_private_key(
    ec.SECP384R1(), default_backend()
    )
    return private_key

def generate_pub_key(private_key):
    public_key = private_key.public_key()
    return public_key

def encode_private_key_pem_format(private_key):
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    return pem.decode()
def encode_public_key_pem_format(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem.decode()
def decode_public_key_byte_format(str_encoded_public_key):
    public_key_obj = serialization.load_pem_public_key(
        str_encoded_public_key.encode(),
        backend=default_backend()
    )
    return public_key_obj.enocde()

def decode_private_key_byte_format(str_encoded_private_key):
    private_key_obj = load_pem_private_key(str_encoded_private_key.encode, password=None, backend=default_backend())
    return private_key_obj.encode()


def CSR_download(request):
    filename = "csr.pem"
    content = request.POST['csr']
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def certificate_download(request):
    filename = "certificate.pem"
    content = request.POST['certificate']
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response