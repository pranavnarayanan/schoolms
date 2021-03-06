# Generated by Django 2.1 on 2018-11-13 05:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EN_UserRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('request_approved_on', models.DateTimeField(default=None, null=True)),
                ('request_raised_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_selected_role', models.BooleanField(default=False)),
                ('related_organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.EN_Organization')),
                ('related_organization_group', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.EN_OrganizationGroup')),
                ('related_user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_user', to='users.EN_Users')),
                ('request_approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_approved_by', to='users.EN_Users')),
                ('request_raised_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='request_raised_by', to='users.EN_Users')),
            ],
            options={
                'db_table': 'en_user_roles',
            },
        ),
        migrations.CreateModel(
            name='TL_Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'tl_roles',
            },
        ),
        migrations.AddField(
            model_name='en_userroles',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='roles.TL_Roles'),
        ),
        migrations.AddField(
            model_name='en_userroles',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.EN_Users'),
        ),
        migrations.AlterUniqueTogether(
            name='en_userroles',
            unique_together={('user', 'role', 'related_organization', 'related_organization_group', 'related_user')},
        ),
    ]
