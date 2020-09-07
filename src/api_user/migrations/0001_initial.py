# Generated by Django 2.2.7 on 2020-09-01 09:17

import api_user.models.photo
import api_user.models.profile
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'hr_users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=255, null=True)),
                ('personal_email', models.EmailField(max_length=255, null=True)),
                ('identity_number', models.CharField(max_length=20, null=True, validators=[django.core.validators.RegexValidator(message='A valid integer is required.', regex='^\\d+$')])),
                ('birth_day', models.DateField(null=True)),
                ('phone', models.CharField(max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='A valid integer is required.', regex='^\\d+$'), django.core.validators.MinLengthValidator(9)])),
                ('teams', models.CharField(max_length=100, null=True)),
                ('account_number', models.CharField(max_length=255, null=True)),
                ('bank', models.CharField(choices=[('No bank', 'No bank'), ('ABBANK', 'ABBANK'), ('ACB', 'ACB'), ('AGRIBANK', 'AGRIBANK'), ('BACABANK', 'BACABANK'), ('BIDV', 'BIDV'), ('DONGABANK', 'DONGABANK'), ('EXIMBANK', 'EXIMBANK'), ('HDBANK', 'HDBANK'), ('IVB', 'IVB'), ('JCB', 'JCB'), ('MASTERCARD', 'MASTERCARD'), ('MBBANK', 'MBBANK'), ('MSBANK', 'MSBANK'), ('NAMABANK', 'NAMABANK'), ('NCB', 'NCB'), ('OCB', 'OCB'), ('OJB', 'OJB'), ('PVCOMBANK', 'PVCOMBANK'), ('SACOMBANK', 'SACOMBANK'), ('SAIGONBANK', 'SAIGONBANK'), ('SCB', 'SCB'), ('SHB', 'SHB'), ('TECHCOMBANK', 'TECHCOMBANK'), ('TPBANK', 'TPBANK'), ('UPI', 'UPI'), ('VIB', 'VIB'), ('VIETCAPITALBANK', 'VIETCAPITALBANK'), ('VIETCOMBANK', 'VIETCOMBANK'), ('VIETINBANK', 'VIETINBANK'), ('VISA', 'VISA'), ('VNMART', 'VNMART'), ('VNPAYQR', 'VNPAYQR'), ('VPBANK', 'VPBANK')], default='No bank', max_length=10, null=True)),
                ('image', models.ImageField(blank=True, max_length=255, null=True, upload_to=api_user.models.profile.name_file)),
                ('join_date', models.DateField(default=django.utils.timezone.now)),
                ('lunch', models.BooleanField(default=False)),
                ('lunch_weekly', models.CharField(max_length=20, null=True)),
                ('veggie', models.BooleanField(default=False)),
                ('line_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_user.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'hr_profiles',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('photo', models.ImageField(blank=True, max_length=255, null=True, upload_to=api_user.models.photo.name_file)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photo', to='api_user.Profile')),
            ],
            options={
                'db_table': 'hr_photos',
            },
        ),
    ]
