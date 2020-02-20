from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone

from api.constants import Banks
from api.models import TimeStampedModel, User


def name_file(instance, filename):
    return '/'.join(['images', str(instance.id), filename])


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, null=True)
    personal_email = models.EmailField(max_length=255, null=True)
    identity_number = models.CharField(max_length=20, null=True, validators=[
        RegexValidator(regex='^\d+$', message='A valid integer is required.')])
    birth_day = models.DateField(null=True)
    phone = models.CharField(max_length=11, null=True, validators=[
        RegexValidator(regex='^\d+$', message='A valid integer is required.'),
        MinLengthValidator(9)])
    teams = models.CharField(max_length=100, null=True)
    account_number = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=10, choices=Banks.BANKS, null=True, default=Banks.No)
    image = models.ImageField(upload_to=name_file, max_length=255, blank=True, null=True)
    join_date = models.DateField(default=timezone.now)
    lunch = models.BooleanField(default=False)
    lunch_weekly = models.CharField(max_length=20, null=True)
    veggie = models.BooleanField(default=False)
