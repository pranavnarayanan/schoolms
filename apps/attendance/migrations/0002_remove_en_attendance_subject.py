# Generated by Django 2.1 on 2019-03-27 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='en_attendance',
            name='subject',
        ),
    ]