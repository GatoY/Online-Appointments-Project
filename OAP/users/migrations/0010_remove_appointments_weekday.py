# Generated by Django 2.0.4 on 2018-05-16 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20180516_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointments',
            name='weekday',
        ),
    ]
