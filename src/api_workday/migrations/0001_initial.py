# Generated by Django 2.2.7 on 2020-06-11 03:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lunchdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('veggie', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'hr_lunchdate',
            },
        ),
        migrations.CreateModel(
            name='ProposeLeave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('start', models.DateField(null=True)),
                ('end', models.DateField(null=True)),
                ('lunch', models.CharField(default='No', max_length=255)),
                ('start_hour', models.CharField(max_length=255, null=True)),
                ('end_hour', models.CharField(max_length=255, null=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('status', models.CharField(default='Pending', max_length=255)),
                ('comments', models.CharField(max_length=255, null=True)),
                ('profile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='leave', to='api_user.Profile')),
            ],
            options={
                'db_table': 'hr_propose_leave',
            },
        ),
        migrations.CreateModel(
            name='Lunch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_date', to='api_workday.Lunchdate')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lunch_profile', to='api_user.Profile')),
            ],
            options={
                'db_table': 'hr_lunch',
            },
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('date', models.DateField(null=True)),
                ('title', models.CharField(max_length=255, null=True)),
                ('content', models.CharField(default=None, max_length=255, null=True)),
                ('reason', models.CharField(default=None, max_length=255, null=True)),
                ('type', models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Full day', 'Full day')], default='Full day', max_length=255, null=True)),
                ('profile', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='date', to='api_user.Profile')),
            ],
            options={
                'db_table': 'hr_date',
            },
        ),
    ]
