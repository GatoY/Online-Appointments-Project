from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout


def home(request):
    return render(request, 'users/home.html')


def info(request):
    return render(request, 'users/info.html')


def doginfo(request):
    return render(request, 'users/doginfo.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('users/home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', context={'form': form})

    def logout(request):
        logout(request)
        return redirect('users/login')

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
