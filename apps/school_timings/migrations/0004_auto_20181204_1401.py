# Generated by Django 2.1 on 2018-12-04 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_timings', '0003_auto_20181204_1218'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='en_schooltimings',
            name='assembly_on_days',
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='assembly_on_friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='assembly_on_monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='assembly_on_saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='assembly_on_sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='assembly_on_thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='assembly_on_tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='assembly_on_wednesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='class_on_friday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='class_on_monday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='class_on_saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='class_on_sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='class_on_thursday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='class_on_tuesday',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='en_schooltimings',
            name='class_on_wednesday',
            field=models.BooleanField(default=True),
        ),
    ]
