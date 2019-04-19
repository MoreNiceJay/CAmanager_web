from django.shortcuts import render
import sys, json, random, hashlib, calendar,time, datetime, os, random
import ast
from cryptography.fernet import Fernet
from django.shortcuts import redirect
from django.http import Http404, HttpResponse
import json
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption,load_pem_private_key
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.x509 import load_pem_x509_csr
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.backends import default_backend
from django.conf import settings
import pycountry
from . models import CSR
from accounts.models import User
from . forms import CSRForm
from . import utility

def start(request):
    return render(request, 'CSR/csr.html', {})

def decoder(request):
    return render(request, 'CSR/decoder.html', {})

def create(request):
    if request.method == 'POST':
        form = CSRForm(request.POST)
        if form.is_valid():
            csr = form.save(commit=False)
            algorithm = csr.algorithm
            private_key = utility.generate_private_key(algorithm)
            public_key = utility.generate_pub_key(private_key)
            private_key_in_pem = utility.encode_private_key_pem_format(private_key)
            public_key_in_pem = utility.encode_public_key_pem_format(public_key)
            encoded_private_key = utility.encode_in_Base64(private_key_in_pem)
            encoded_public_key = utility.encode_in_Base64(public_key_in_pem)

            temp_csr = utility.generate_CSR(csr.country, csr.state, csr.locality, csr.organization, csr.common_name, csr.domain, private_key)
            csr_pem = utility.encode_CSR_in_pem_format(temp_csr)
            
            print(type(csr_pem))

            csr.user = request.user
            csr.private_key = encoded_private_key
            csr.public_key = encoded_public_key
            csr.pem = csr_pem
            csr.save()
        return HttpResponse(csr_pem)
        #return render(request, 'CSR/create.html', {'csr':csr_pem, 'hi':"heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","private_key":private_key_in_pem, "public_key":public_key_in_pem, })

    else:
        form = CSRForm()
        return render(request, 'CSR/create.html',{})

def decoder_info(request):
    return render(request, 'CSR/decoder_info.html', {})

def countries_in_JSON(request):
    countries = {country.alpha_2 : country.name for country in pycountry.countries}  
    data = json.dumps(countries)
    return HttpResponse(data)

def retrive_CSR_table_data(request):
    try:
        user = User.objects.get(username=request.user.username)
        csrs = CSR.objects.filter(user=user)

    except:              
        raise NoUserError
    data = []
    for csr in csrs:
        data.append({'organization':csr.organization,'domain':csr.domain,'algorithm':csr.algorithm,'created_date':csr.created_date.strftime("%Y/%m/%d") })
    data = json.dumps(data)
    return HttpResponse(data)

def email_csr(request):
    filename = "csr.pem"
    content = request.POST['csr']
    print(content)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def download_csr(request):
    filename = "csr.pem"
    content = request.POST['csr']
    print(content)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def download_private_key(request):
    filename = "private_key.pem"
    content = request.POST['private_key']
    print(content)

    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

def download_public_key(request):
    print("lllllllllllllllllllllllllllllllllllllllllll")
    filename = "public_key.pem"
    content = request.POST['public_key']
    print(request.POST)
    print(content)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response

