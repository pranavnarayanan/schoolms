# Generated by Django 2.1 on 2019-01-07 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_en_users_activation_token'),
        ('documents', '0007_auto_20190107_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='en_documents',
            name='name',
            field=models.CharField(default='Name', max_length=100),
        ),
        migrations.AddField(
            model_name='en_documents',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.EN_Users'),
        ),
        migrations.AlterField(
            model_name='en_documents',
            name='unique_name',
            field=models.CharField(default=11, max_length=500, unique=True),
        ),
    ]
