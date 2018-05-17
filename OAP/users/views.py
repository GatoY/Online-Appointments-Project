from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, InfoForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from .models import userInfo, Dog, Appointments
import time
import re

WEEK = 3
YEAR = 2018
now = timezone.now()


def home(request):
    return render(request, 'users/home.html')


@csrf_protect
def info(request):
    current_user = request.user
    try:
        userinfo = userInfo.objects.get(user=current_user)
    except:
        userinfo = None
    if request.method == 'POST':
        if userinfo is None:
            userinfo = userInfo()
        userinfo.user = current_user
        userinfo.address = request.POST.get('address')
        userinfo.mobile = request.POST.get('mobile')
        userinfo.workPhone = request.POST.get('workPhone')
        userinfo.home = request.POST.get('home')
        userinfo.save()
        return render(request, 'users/info.html', context={
            'flag': 1,
            'address': userinfo.address,
            'mobile': userinfo.mobile,
            'workPhone': userinfo.workPhone,
            'home': userinfo.home})
    if userinfo is not None:
        return render(request, 'users/info.html', context={'address': userinfo.address,
                                                           'mobile': userinfo.mobile,
                                                           'workPhone': userinfo.workPhone,
                                                           'home': userinfo.home})
    else:
        return render(request, 'users/info.html')


def petslist(request):
    current_user = request.user
    petslist = Dog.objects.filter(owner=current_user)
    context = {'petslist': petslist}
    return render(request, 'users/petslist.html', context)


def editdoginfo(request, dogid):
    current_user = request.user
    dog = Dog.objects.get(owner=current_user, id=dogid)
    print(dog.dob)

    if request.method == 'POST':
        dog.owner = current_user
        name = request.POST.get('name')
        if name is not None and name != '':
            dog.name = name
        print(dog.name)
        breed = request.POST.get('breed')
        if breed is not None and name != '':
            dog.breed = breed
        dob = request.POST.get('dob')
        if dob is not None and dob != '':
            dog.dob = dob
        print(dog.dob)
        dog.save()

        return redirect('../../petslist')

    return render(request, 'users/editdoginfo.html', context={
        'id':dogid,
        'name': dog.name,
        'breed': dog.breed,
        'dob': dog.dob})


def doginfo(request):
    current_user = request.user
    if request.method == 'POST':
        dog = Dog()
        dog.owner = current_user
        dog.name = request.POST.get('name')
        dog.breed = request.POST.get('breed')
        dog.dob = request.POST.get('dob')
        dog.save()
        return redirect('../../users/petslist')
    else:
        return render(request, 'users/doginfo.html')


@csrf_protect
def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
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


# def schedule(request):
#     return render(request, 'users/schedule.html')


def mybook(request):
    tmp = time.localtime()
    date = time.strftime('%m-%d', tmp)
    datelist = generateDatelist(date, WEEK)
    current_user = request.user
    appointmentsList = Appointments.objects.filter(endtime__gte=now, user=current_user)
    week = [0] * WEEK
    context = {'appointmentsList': appointmentsList, 'week': week, 'datelist': datelist}
    return render(request, 'users/mybook.html', context)


class datelist_detail():
    year = 0
    month = 0
    day = 0

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


def generateDatelist(startDate, WEEK):
    datelist = []
    # datelist.append(startDate)
    month = int(startDate[:2])
    day = int(startDate[3:5]) - 1
    for i in range(0, 5 * WEEK):
        # print(1)
        day = day + 1
        if day < 29:
            pass
        elif day == 29 and month == 2:
            month = 3
            day = 1
        elif day == 31 and month % 2 == 0:
            if month == 12:
                month = 1
            else:
                month = month + 1
            day = 1
        elif day == 32:
            month = month + 1
            day = 1
        else:
            pass
        tmp = datelist_detail(YEAR, month, day)
        # addDate = str(day) + '-' + str(month) + '-' + str(YEAR)
        # print(addDate)
        datelist.append(tmp)
    return datelist


def availbleschedule(request):
    tmp = time.localtime()
    date = time.strftime('%m-%d', tmp)
    # print('start '+ date)
    datelist = generateDatelist(date, WEEK)
    # for i in datelist:
    #     print(i)
    # weekday = time.strftime('%w', tmp)
    appointmentsList = Appointments.objects.filter(endtime__gte=now)
    week = [0] * WEEK
    context = {'appointmentsList': appointmentsList, 'week': week, 'datelist': datelist}
    return render(request, 'users/availbleschedule.html', context)


def format_datetime(datetime):
    year = datetime[6:10]
    month = datetime[0:2]
    day = datetime[3:5]
    pattern_hour = re.compile(r'\s(.+):')
    hour = pattern_hour.search(datetime).group(1)
    pattern_min = re.compile(r':(.+)\s')
    min = pattern_min.search(datetime).group(1)
    ampm = datetime[-2:]
    if ampm == 'PM':
        hour = int(hour) + 12
    if int(hour) < 10:
        hour = '0' + str(hour)
    # if int(min)<10:
    #     min = '0'+str(min)
    value = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(min)
    return value


def booking(request):
    current_user = request.user
    dog_list = Dog.objects.filter(owner=current_user)
    if request.method == 'POST':
        # print(2)

        # form = MakeAppointmentsForm(request.POST)
        # print(3)
        # print(request.POST.get('dog', ''))
        # print(form)
        # if form.is_valid():
        appointment = Appointments()
        appointment.user = current_user
        # print(current_user)
        # print(form.cleaned_data.get('starttime'))
        dogname = request.POST.get('dog')
        # print(form.cleaned_data['dog'])
        # print(dogname)
        thedog = Dog.objects.get(name=dogname, owner=current_user)
        print(thedog.breed)
        thedog.save()

        appointment.dog = thedog
        appointment.msg = request.POST.get('msg')
        appointment.starttime = format_datetime(request.POST.get('starttime'))
        appointment.endtime = format_datetime(request.POST.get('endtime'))
        print('1')
        thedog.save()
        appointment.save()
        return render(request, 'users/bookSuccess.html', context={'dogname': dogname,
                                                                  'starttime': appointment.starttime,
                                                                  'endtime': appointment.starttime,
                                                                  'msg': appointment.msg})
        # return redirect('../../users/home')
        # form = MakeAppointmentsForm()
    # return render(request, 'users/login.html', context={'form': form})
    return render(request, 'users/booking.html', context={'dog_list': dog_list})


def bookavailable(request):
    return render(request, 'users/event-available.html')


def bookbooked(request):
    return render(request, 'users/event-booked.html')


def bookDetail(request):
    return render(request, 'users/bookDetail.html')

# def bookSuccess(request):
# return render(request, 'users/bookSuccess.html')
# Create your views here.
