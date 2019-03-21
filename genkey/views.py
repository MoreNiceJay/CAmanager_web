from django.shortcuts import render
from .forms import firstFrom
from django.shortcuts import redirect

# Create your views here.
def post_list(request):
    return render(request, 'genkey/post_list.html', {})

def configure_CA_subject_name(request):
    print("여기!")
    if request.method == 'POST':
        form = firstFrom(request.POST)
        if form.is_valid():
            print(request)
            print(form.title)
            print("good")
            return redirect('configure_CA_key_algorithm',)
    else:
        form = firstFrom()
        print("no good")

    return render(request, 'genkey/configure_CA_subject_name.html', {'form': form})

def configure_CA_key_algorithm(request):
    print("알고리즘!")

    return render(request, 'genkey/configure_CA_key_algorithm.html', {})