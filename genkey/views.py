from django.shortcuts import render
from .forms import subjectForm, algorithmForm, CRLForm
from django.shortcuts import redirect
from django.http import Http404
import json
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

    form = algorithmForm()
    return render(request, 'genkey/configure_CA_key_algorithm.html', {'form':form, 'organization':organization, 'organization_unit':organization_unit,
                  'country':country, 'state':state, 'locality':locality , 'common_name':common_name})

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
    prev_form = CRLForm(request.POST)
    if prev_form.is_valid():
        CRL_name = prev_form.cleaned_data['CRL_name']
        valid_period = prev_form.cleaned_data['valid_period']
    algorithm = request.POST['algorithm']
    organization = request.POST['organization']
    organization_unit = request.POST['organization_unit']
    country = request.POST['country']
    state = request.POST['state']
    locality = request.POST['locality']
    common_name = request.POST['common_name']

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
    if algorithm == "rsa_2048":
        ca.private_key = generate_RSA_private_key(2048)
        print(ca.private_key)
    elif algorithm == "rsa_4096":
        ca.private_key = generate_RSA_private_key(4096)
        print(ca.private_key)

    elif algorithm == "ecdsa_p256":
        ca.private_key = generate_ECP256_private_key()
        print(ca.private_key)

    elif algorithm == "ecdsa_p384":
        ca.private_key = generate_ECP384_private_key()
        print(ca.private_key)


    ca.public_key = generate_pub_key(ca.private_key)
    ca.save()

    return render(request, 'genkey/review_and_create.html' )


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

