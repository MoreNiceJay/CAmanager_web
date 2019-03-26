from django.shortcuts import render
from .forms import subjectForm, algorithmForm, CRLForm, CA_choice
from django.shortcuts import redirect
from django.http import Http404
import json
from .models import Issuer
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.x509 import load_pem_x509_csr
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend

from .models import CA
# Create your views here.
def post_list(request):
    print(type(generate_ECP256_private_key()))
    return render(request, 'genkey/post_list.html', {})

def configure_CA_subject_name(request):
    form = subjectForm()
    return render(request, 'genkey/configure_CA_subject_name.html', {'form': form} )


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
    print("요기요")
    print(request.POST)
    prev_form = CRLForm(request.POST)
    if prev_form.is_valid():
        CRL_name = prev_form.cleaned_data['CRL_name']
        valid_period = prev_form.cleaned_data['valid_period']


    organization = request.POST['organization']
    algorithm = request.POST['algorithm']
    organization_unit = request.POST['organization_unit']
    country = request.POST['country']
    state = request.POST['state']
    locality = request.POST['locality']
    common_name = request.POST['common_name']
    domain = request.POST['domain']

    ca = CA()
    ca.algorithm = algorithm
    ca.organization = organization
    ca.organization_unit = organization_unit
    ca.country = country
    ca.state = state
    ca.locality = locality
    ca.common_name = common_name
    ca.CRL_name = CRL_name
    ca.valid_period = valid_period
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
    CA_public_key = generate_pub_key(ca.private_key)
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
    issuer = Issuer.objects.get(pk=int(issuer_pk))

    CA_public_key = encode_public_key_pem_format()

    csr = load_pem_x509_csr(request.POST['csr'].encode(), backend=default_backend())

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
        x509.NameAttribute(NameOID.COUNTRY_NAME, issuer.country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, issuer.state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, issuer.locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, issuer.organization),
        x509.NameAttribute(NameOID.COMMON_NAME, issuer.common_name),
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
        x509.SubjectAlternativeName([x509.DNSName(issuer.domain)]),
        critical=False,
        # Sign our certificate with our private key
    ).sign(CA_private_key, hashes.SHA256(), default_backend())
    # Write our certificate out to disk.



    return render(request, 'genkey/export_certificate.html' )






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
def encode_public_key_pem_format(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )