# Generated by Django 4.0 on 2022-01-09 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_admindata_gender_students_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admindata',
            name='special_token',
        ),
        migrations.RemoveField(
            model_name='students',
            name='special_token',
        ),
    ]
