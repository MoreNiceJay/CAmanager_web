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


def start(request):
    return render(request, 'CSR/csr.html', {})

def decoder(request):
    return render(request, 'CSR/decoder.html', {})

def create(request):
    print(request)
    return render(request, 'CSR/create.html', {})
def decoder_info(request):
    return render(request, 'CSR/decoder_info.html', {})

def get_countries_in_JSON(request):
    countries = {country.alpha_2 : country.name for country in pycountry.countries}  
    data = json.dumps(countries)
    return HttpResponse(data)

