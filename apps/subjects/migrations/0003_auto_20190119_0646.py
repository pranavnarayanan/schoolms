# Generated by Django 2.1.4 on 2019-01-19 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_auto_20190119_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='en_classsubjects',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.EN_Organization'),
        ),
    ]
