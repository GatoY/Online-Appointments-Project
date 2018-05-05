from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=80, default='', blank =True, null =True)
    mobile = models.IntegerField(default=None, blank = True, null =True)
    home = models.IntegerField(blank=True,default=None, null =True)
    workPhone=models.IntegerField(blank=True, default=None, null =True)
    
    class Meta(AbstractUser.Meta):
        pass

class Dog(models.Model):
    name = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    dob =models.DateTimeField('date of birth')
    owner = models.ForeignKey('User', on_delete = models.CASCADE)
# Create your models here.
