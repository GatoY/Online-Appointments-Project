from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = models.EmailField(max_length=50, unique=True)

    class Meta(AbstractUser.Meta):
        pass


class userInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=80, default='', blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[phone_regex], max_length=17)  # validators should be a list
    workPhone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    home = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list


class Dog(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    dob = models.DateTimeField('date of birth')
    owner = models.ForeignKey('User', on_delete=models.CASCADE)


# Create your models here.

# class TimeSchedule(models.Model):
#     weekday = models.DateField()

class Appointments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    msg = models.CharField(max_length=140, default=' ', blank=True, null=True)
    starttime = models.DateTimeField()  # y-m-d-h-m-s
    endtime = models.DateTimeField()

    def getyear(self):
        return self.starttime.year

    def getmonth(self):
        return self.starttime.month

    def getday(self):
        return self.starttime.day

    def getstarthour(self):
        return self.starttime.hour

    def getstartmin(self):
        min = self.starttime.minute
        if int(min) < 10:
            min = '0' + str(min)
        return min

    def getendhour(self):
        return self.endtime.hour

    def getendmin(self):
        min = self.endtime.minute
        if int(min) < 10:
            min = "0" + str(min)
        return min
    # weekday = models.IntegerField() #0-6
