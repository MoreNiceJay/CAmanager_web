
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import User
from . forms import User as UserForm
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if request.is_ajax():
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                return HttpResponse("okay")  
            except:
                #없을때
                return HttpResponse("no")
        else:
            if form.is_valid():
                print(form.cleaned_data['email'])
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                try:
                    user.save()
                    return redirect('index')
                except Exception as ex:
                    return redirect('index')
    else:
        form = User()
    return render(request, 'registration/register.html', {})
#
# def password_reset(request):
#     return render(request, 'registration/password_reset.html', {})

def profile(request):
    
    return render(request, 'registration/profile.html', {})

def email_is_valid(email):
    if (email):
        pass
        return true
    else:
        pass
        return false
