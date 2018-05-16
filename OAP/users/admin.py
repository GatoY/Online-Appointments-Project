from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User,userInfo,Dog,Appointments

admin.site.register(User)
admin.site.register(userInfo)
admin.site.register(Dog)
admin.site.register(Appointments)
