# Generated by Django 2.1b1 on 2018-12-01 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20181202_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='en_documents',
            name='data_file',
            field=models.FileField(max_length=500, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='en_documents',
            name='file_description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='en_documents',
            name='name',
            field=models.CharField(max_length=500, unique=True),
        ),
        migrations.AlterField(
            model_name='en_documents',
            name='tag',
            field=models.CharField(max_length=100, null=True),
        ),
    ]