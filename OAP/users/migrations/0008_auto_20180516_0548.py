# Generated by Django 2.0.4 on 2018-05-16 05:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20180512_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookform',
            old_name='time',
            new_name='endtime',
        ),
        migrations.AddField(
            model_name='bookform',
            name='starttime',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
