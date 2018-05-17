"""OAP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = 'users'

urlpatterns = [
    #path('', views.home),
    #path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userLogout/', views.userLogout, name = 'userLogout'),
    path('home/', views.home, name ='home'),
    path('info/', views.info, name ='info'),
    path('doginfo/', views.doginfo, name ='doginfo'),
    path('petslist/', views.petslist, name ='petslist'),
    # path('schedule/', views.schedule, name ='schedule'),
    path('mybook/', views.mybook, name ='mybook'),
    path('booking/', views.booking, name ='booking'),
    path('availbleschedule', views.availbleschedule, name ='availbleschedule'),
    path('availbleschedule/bookDetail', views.bookDetail, name ='bookDetail'),
    path('availbleschedule/event-available', views.bookavailable, name ='bookavailable'),
    path('availbleschedule/event-booked', views.bookbooked, name ='bookbooked'),
    #path('bookSuccess', views.bookSuccess, name ='bookSuccess'),

    # path('users/', include('users.urls')),
    # path('users/', include('django.contrib.auth.urls')),
]

