# Generated by Django 2.1.2 on 2018-12-01 12:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181130_0010'),
        ('documents', '0002_auto_20181201_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='en_documents',
            name='uploaded_by',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='users.EN_Users'),
            preserve_default=False,
        ),
    ]
