# Generated by Django 2.1 on 2019-01-07 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_auto_20181202_0029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='en_documents',
            name='data_file',
        ),
        migrations.RemoveField(
            model_name='en_documents',
            name='file_description',
        ),
        migrations.RemoveField(
            model_name='en_documents',
            name='name',
        ),
        migrations.RemoveField(
            model_name='en_documents',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='en_documents',
            name='type',
        ),
        migrations.RemoveField(
            model_name='en_documents',
            name='uploaded_by',
        ),
        migrations.RemoveField(
            model_name='en_documents',
            name='uploaded_on',
        ),
    ]