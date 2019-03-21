from django import forms
import pycountry

class subjectForm(forms.Form):
    organization = forms.CharField()
    organization_unit = forms.CharField()
    country = forms.ChoiceField(choices=[(country.alpha_2, country.name) for country in pycountry.countries])
    state = forms.CharField()
    locality = forms.CharField()
    common_name = forms.CharField()

class algorithmForm(forms.Form):
    CHOICES = (('rsa_2048', 'RSA 2048', ), ('rsa_4096','RSA 4096', ) , ('ecdsa_p256','ECDSA P256', ), ('ecdsa_p384','ECDSA P384', ))
    algorithm = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class CRLForm(forms.Form):
    CRL_name = forms.CharField()
    valid_period = forms.CharField()

