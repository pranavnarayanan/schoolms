# Generated by Django 2.1b1 on 2018-11-13 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utilities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EN_Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=12, unique=True)),
                ('school_name', models.CharField(max_length=12)),
                ('started_date', models.DateField()),
                ('display_picture', models.CharField(max_length=100, null=True)),
                ('mobile_number_1', models.CharField(max_length=10)),
                ('mobile_number_2', models.CharField(max_length=10)),
                ('landline_number_1', models.CharField(max_length=13)),
                ('landline_number_2', models.CharField(max_length=13, null=True)),
                ('email_id', models.EmailField(max_length=254, null=True)),
                ('website', models.CharField(max_length=100, null=True)),
                ('publish_your_site', models.BooleanField(default=True)),
                ('street', models.CharField(max_length=100, null=True)),
                ('registration_id', models.CharField(max_length=100, null=True, unique=True)),
                ('account_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='utilities.TL_AccountStatus')),
            ],
            options={
                'db_table': 'en_organization',
            },
        ),
        migrations.CreateModel(
            name='EN_OrganizationGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=12, unique=True)),
                ('group_name', models.CharField(max_length=100)),
                ('logo', models.CharField(max_length=100, null=True)),
                ('website', models.CharField(max_length=100, null=True)),
                ('publish_your_site', models.BooleanField(default=False)),
                ('account_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='utilities.TL_AccountStatus')),
            ],
            options={
                'db_table': 'en_organization_group',
            },
        ),
        migrations.CreateModel(
            name='TL_Affiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField(null=True)),
            ],
            options={
                'db_table': 'tl_affiliation',
            },
        ),
        migrations.CreateModel(
            name='TL_InstitutionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=40, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'tl_institution_type',
            },
        ),
        migrations.AddField(
            model_name='en_organization',
            name='affiliation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.TL_Affiliation'),
        ),
        migrations.AddField(
            model_name='en_organization',
            name='mobile_country_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='utilities.EN_Country'),
        ),
        migrations.AddField(
            model_name='en_organization',
            name='organization_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.EN_OrganizationGroup'),
        ),
        migrations.AddField(
            model_name='en_organization',
            name='organization_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.TL_InstitutionType'),
        ),
        migrations.AddField(
            model_name='en_organization',
            name='zipcode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='utilities.EN_Zipcode'),
        ),
        migrations.AlterUniqueTogether(
            name='en_organizationgroup',
            unique_together={('group_name', 'website')},
        ),
        migrations.AlterUniqueTogether(
            name='en_organization',
            unique_together={('school_name', 'zipcode', 'registration_id')},
        ),
    ]
