# Generated by Django 2.2.7 on 2020-09-04 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_workday', '0002_auto_20200904_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dateoff',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
