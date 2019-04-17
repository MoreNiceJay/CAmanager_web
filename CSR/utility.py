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

def generate_private_key(algorithm):
    private_key = None
    if algorithm == "RSA_2048":
        private_key = generate_RSA_private_key(2048)
    elif algorithm == "RSA_4096":
        private_key = generate_RSA_private_key(4096)
    elif algorithm == "ECDSA_P256":
        private_key = generate_ECP256_private_key()
    elif algorithm == "ECDSA_P384":
        private_key = generate_ECP384_private_key()
    else:
        raise AlgorithmMismatchError
    return private_key

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
    return pem

def encode_public_key_pem_format(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem

def encode_in_Base64(key_in_pem_format):
    with open("base64.key", "rb") as f:
        key = f.read()
    f = Fernet(key)
    token = f.encrypt(key_in_pem_format)
    return token.decode()

def decode_Base64(encrypted_key_token):
    with open("base64.key", "rb") as f:
        key = f.read()
    f = Fernet(key)
    return f.decrypt(encrypted_key_token.encode())


def generate_CSR(country,state,locality,organization,common_name,domain,private_key):
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
    ).sign(private_key, hashes.SHA256(), default_backend())
    return csr

def encode_CSR_in_pem_format(temp_csr):
    return temp_csr.public_bytes(serialization.Encoding.PEM).decode()