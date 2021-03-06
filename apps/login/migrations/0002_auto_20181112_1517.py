# Generated by Django 2.1 on 2018-11-12 09:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='en_logincredentials',
            name='current_logged_in_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='en_logincredentials',
            name='last_logged_in_time',
            field=models.DateTimeField(null=True),
        ),
    ]
