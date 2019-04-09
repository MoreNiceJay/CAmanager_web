from django.shortcuts import render, redirect
from django.http import Http404
from mysite import settings
# Create your views here.
def index(request):
    print(settings.BASE_DIR)


    return render(request, 'mainpage/index.html', {})