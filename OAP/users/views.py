from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, 'users/home.html')


def info(request):
    return render(request, 'users/info.html')


def doginfo(request):
    return render(request, 'users/doginfo.html')

@csrf_protect
def login(request):
    if request.method == 'POST':
        print(2)
        form = LoginForm(request.POST)
        print(3)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(4)
        user = authenticate(username=username, password=password)
        print(5)
        if user is not None:
            if user.is_active:
                login(request, user)
                print(1)
                return redirect('users/home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', context={'form': form})

def logout(request):
    logout(request)
    return redirect('users/login')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/users/login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})


def schedule(request):
    return render(request, 'users/schedule.html')


def mybook(request):
    return render(request, 'users/mybook.html')


def booking(request):
    return render(request, 'users/booking.html')

# Create your views here.
