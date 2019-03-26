from django import forms
import pycountry
from .models import Issuer
from django.forms import ModelChoiceField

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id

class subjectForm(forms.Form):
    organization = forms.CharField()
    organization_unit = forms.CharField()
    country = forms.ChoiceField(choices=[(country.alpha_2, country.name) for country in pycountry.countries])
    state = forms.CharField()
    locality = forms.CharField()
    common_name = forms.CharField()
    domain = forms.CharField()

class algorithmForm(forms.Form):
    CHOICES = (('rsa_2048', 'RSA 2048', ), ('rsa_4096','RSA 4096', ) , ('ecdsa_p256','ECDSA P256', ), ('ecdsa_p384','ECDSA P384', ))
    algorithm = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class CRLForm(forms.Form):
    CRL_name = forms.CharField()
    valid_period = forms.CharField()

class CA_choice(forms.Form):
    CA = forms.ModelChoiceField(queryset=Issuer.objects.all().order_by('common_name'),)
