# Generated by Django 2.2.7 on 2020-08-30 02:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('team_name', models.CharField(max_length=255)),
                ('team_email', models.EmailField(max_length=255)),
                ('team_leader', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'hr_teams',
            },
        ),
    ]
