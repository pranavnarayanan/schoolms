# Generated by Django 2.1b1 on 2018-11-10 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_up', '0003_auto_20181109_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='en_userregistration',
            name='is_current_address',
            field=models.BooleanField(default=False),
        ),
    ]
