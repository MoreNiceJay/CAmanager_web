
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import User
from . forms import User as UserForm
from django.contrib.auth import login, authenticate

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if request.is_ajax():
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                return HttpResponse("registered")  
            except:
                #없을때
                return HttpResponse("new")
        else:
            if form.is_valid():
                
                user = form.save(commit=False)
                user.username = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user.set_password(password)
                try:
                    user.save()
                    login(request, user)
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

def sign_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate( username=username, password=password)
        if user is not None:
            login(request, user)    
            return redirect('index')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        return render(request, 'registration/login.html', {})