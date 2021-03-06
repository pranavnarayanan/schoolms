# Generated by Django 2.1 on 2019-01-10 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EN_Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('notification_type', models.CharField(max_length=50)),
                ('read_status', models.BooleanField(default=False)),
                ('can_change_read_status_direclty', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'en_notifications',
            },
        ),
    ]
