# Generated by Django 2.1.2 on 2018-12-01 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='en_documents',
            name='file_name',
            field=models.CharField(max_length=30),
        ),
    ]
