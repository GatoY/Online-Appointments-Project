from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, InfoForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from .models import userInfo, Dog


def home(request):
    return render(request, 'users/home.html')


@csrf_protect
def info(request):
    if request.method == 'POST':
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../../users/home')
    else:
        form = InfoForm()
        print(1)
    return render(request, 'users/info.html', context={'form': form})


def doginfo(request):
    return render(request, 'users/doginfo.html')


@csrf_protect
def userLogin(request):
    if request.method == 'POST':
        print(2)
        form = LoginForm(request.POST)
        print(3)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(4)
        user = authenticate(request, username=username, password=password)
        print(5)
        if user is not None:
            if user.is_active:
                login(request, user)
                print(1)
                return redirect('../../users/home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', context={'form': form})


def userLogout(request):
    logout(request)
    return redirect('../../users/userLogin')


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


def bookavailable(request):
    return render(request, 'users/event-available.html')


def bookbooked(request):
    return render(request, 'users/event-booked.html')

def bookDetail(request):
    return render(request, 'users/bookDetail.html')
def bookSuccess(request):
    return render(request, 'users/bookSuccess.html')
# Create your views here.
