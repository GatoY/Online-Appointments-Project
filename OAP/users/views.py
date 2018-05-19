from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, InfoForm
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from .models import userInfo, Dog, Appointments
from .mail import sendEmail, sendSuccessEmail

import time
import re

WEEK = 3
YEAR = 2018
now = timezone.now()


# def sendmail(toemail)
#     print("sending email")
#     send_mail('A reminder for your grooming appointment', 'You have an appointment within 24 hours, please check it.', 'developer@yu.com',
#               ['toemail'], fail_silently=False)
#     print("sent success")

def sendmail():
    now = timezone.now()
    mth = now.month
    hour = now.hour
    minutes = now.min
    second = now.second
    if hour == 11 and minutes == 31 and second == 00:
        print("sending email")
        day = now.day

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
        next = now

        next.day = day
        appointlist = Appointments.objects.filter(starttime__range=[now, next])
        emaillist = []
        for i in appointlist:
            emaillist.append(i.user)
        for touser in emaillist:
            sendEmail(touser)


# TODO email
def home(request):
    sendmail()
    # sendmail('derakhy@gmail.com')
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
        'id': dogid,
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
            return redirect('/users/userLogin')
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


def mybooklist(request):
    current_user = request.user
    appointmentsList = Appointments.objects.filter(endtime__gte=now, user=current_user)
    context = {'appointmentsList': appointmentsList}
    return render(request, 'users/mybooklist.html', context)


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
        appointment.dog = thedog
        appointment.msg = request.POST.get('msg')
        appointment.groomingoptions = request.POST.get('groom')
        appointment.starttime = format_datetime(request.POST.get('starttime'))
        appointment.endtime = format_datetime(request.POST.get('endtime'))
        thedog.save()
        appointment.save()
        msg = 'Book for:' + dogname + ', Option:' + appointment.groomingoptions + ', Start at:' + str(appointment.starttime) + ' To ' + str(appointment.endtime) + ' Message:' + appointment.msg
        sendSuccessEmail(appointment.user.username, msg)
        return render(request, 'users/bookSuccess.html', context={'dogname': dogname,
                                                                  'starttime': appointment.starttime,
                                                                  'endtime': appointment.endtime,
                                                                  'groom': appointment.groomingoptions,
                                                                  'msg': appointment.msg})
        # return redirect('../../users/home')
        # form = MakeAppointmentsForm()
    # return render(request, 'users/login.html', context={'form': form})
    return render(request, 'users/booking.html', context={'dog_list': dog_list})


def cancel(request):
    current_user = request.user
    appointmentsList = Appointments.objects.filter(endtime__gte=now, user=current_user)
    context = {'appointmentsList': appointmentsList}
    return render(request, 'users/cancel.html', context)


def cancelconfirm(request, appid):
    current_user = request.user
    appointment = Appointments.objects.get(id=appid, user=current_user)
    appointment.delete()
    appointmentsList = Appointments.objects.filter(endtime__gte=now, user=current_user)
    context = {'appointmentsList': appointmentsList}
    msg = 'You have cancelled:' + appointment.dog.name + ', Option:' + appointment.groomingoptions + ', Start at:' + str(appointment.starttime) + ' To ' + str(appointment.endtime) + ' Message:' + appointment.msg
    sendSuccessEmail(current_user.username, msg)
    return render(request, 'users/cancel.html', context)


def reschedule(request):
    current_user = request.user
    appointmentsList = Appointments.objects.filter(endtime__gte=now, user=current_user)
    context = {'appointmentsList': appointmentsList}
    return render(request, 'users/reschedule.html', context)


def rescheduledetail(request, appid):
    appointment = Appointments.objects.get(id=appid)
    currentuser = request.user
    username = currentuser.username
    if request.method == 'POST':
        msg = request.POST.get('msg')
        if msg is not None and msg != '':
            appointment.msg = msg
        appointment.groomingoptions = request.POST.get('groom')
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        if starttime is not None and starttime != '':
            appointment.starttime = format_datetime(starttime)
        if endtime is not None and endtime != '':
            appointment.endtime = format_datetime(endtime)
        appointment.save()
        msg = 'Book for:' + appointment.dog.name + ', Option:' + appointment.groomingoptions + ', Start at:' + str(
            appointment.starttime) + ' To ' + str(
            appointment.endtime) + ' Message:' + appointment.msg
        print()
        sendSuccessEmail(username, msg)
        return render(request, 'users/rescheduleSuccess.html', context={'dogname': appointment.dog.name,
                                                                        'groom': appointment.groomingoptions,
                                                                        'starttime': appointment.starttime,
                                                                        'endtime': appointment.starttime,
                                                                        'msg': appointment.msg})
    return render(request, 'users/rescheduledetail.html', context={'appointment': appointment})


def bookavailable(request):
    return render(request, 'users/event-available.html')


def bookbooked(request):
    return render(request, 'users/event-booked.html')


def bookDetail(request):
    return render(request, 'users/bookDetail.html')

# def bookSuccess(request):
# return render(request, 'users/bookSuccess.html')
# Create your views here.
