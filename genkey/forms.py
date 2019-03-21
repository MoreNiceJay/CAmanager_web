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
    CHOICES = (('RSA 2048', 'rsa_2048',), ('RSA 4096', 'rsa_4096',) , ('ECDSA P256', 'ecdsa_p256',), ('ECDSA P384', 'ecdsa_p384',))
    algorithm = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class CRLForm(forms.Form):
    pass