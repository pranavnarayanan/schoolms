# Generated by Django 2.1 on 2018-11-14 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EN_Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_datetime', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=500)),
                ('read_status', models.BooleanField(default=False)),
                ('send_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send_by', to='users.EN_Users')),
                ('send_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send_to', to='users.EN_Users')),
            ],
            options={
                'db_table': 'en_message',
            },
        ),
    ]