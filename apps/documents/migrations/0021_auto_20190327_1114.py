# Generated by Django 2.1 on 2019-03-27 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0020_auto_20190119_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='en_documents',
            name='unique_name',
            field=models.CharField(default='doc_291', max_length=500, unique=True),
        ),
    ]
