from django.shortcuts import render, redirect
from .forms import RegisterForm

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context = {'form':form})



# Create your views here.
