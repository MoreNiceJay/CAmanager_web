from django.shortcuts import render
from .forms import subjectForm, algorithmForm, CRLForm
from django.shortcuts import redirect
from django.http import Http404
import json

# Create your views here.
def post_list(request):
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
        print("hihi")
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
        organization = prev_form.cleaned_data['organization']
        organization_unit = prev_form.cleaned_data['organization_unit']
        country = prev_form.cleaned_data['country']
        state = prev_form.cleaned_data['state']
        locality = prev_form.cleaned_data['locality']
        common_name = prev_form.cleaned_data['common_name']
    return render(request, 'genkey/review_and_create.html' )
