from django.shortcuts import render
from .forms import subjectForm, algorithmForm
from django.shortcuts import redirect
import pycountry

# Create your views here.
def post_list(request):



    return render(request, 'genkey/post_list.html', {})

def configure_CA_subject_name(request):
    if request.method == 'POST':
        form = subjectForm(request.POST)
        if form.is_valid():
            # print(request.POST['organization'])
            # print(form.cleaned_data['organization'])
            # print(form.cleaned_data['days'])
            # print("good")
            #print(request.POST)
            return redirect('configure_CA_key_algorithm', )
    else:
        form = subjectForm()
    return render(request, 'genkey/configure_CA_subject_name.html', {'form': form})


def configure_CA_key_algorithm(request):
    print(request.POST)
    print(request.POST['hi'])
    if request.method == 'POST':
        form = algorithmForm(request.POST)
        if form.is_valid():
            # print(request.POST['organization'])
            # print(form.cleaned_data['organization'])
            # print(form.cleaned_data['days'])
            # print("good")
            #print(request.POST)
            args = {'data':"data"}
            return render(request, 'genkey/configure_certificate_revocation.html',args )

    # elif request.method == 'GET':
    #     form = algorithmForm()
    #     return redirect('configure_certificate_revocation')
    else:
        print("empty in the algorithm")
        form = algorithmForm()

    return render(request, 'genkey/configure_CA_key_algorithm.html', {'organization': request.POST['organization'],'country':request.POST['country']})

def configure_certificate_revocation(request):
    print(request.POST)
    return render(request, 'genkey/configure_certificate_revocation.html', {})