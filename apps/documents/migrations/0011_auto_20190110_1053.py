# Generated by Django 2.1 on 2019-01-10 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0010_auto_20190107_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='en_documents',
            name='unique_name',
            field=models.CharField(default=36, max_length=500, unique=True),
        ),
    ]