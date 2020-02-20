#!/usr/bin/env python

# author Huy
# date 12/8/2019
import calendar
import datetime

from rest_framework.exceptions import ValidationError

from api.models import Lunch, Lunchdate
from api.services import BaseService, DateService
from lunarcalendar import Converter, Solar, Lunar, DateNotExist


class LunchService(BaseService):

    @staticmethod
    def get_current_date():
        current_day = datetime.datetime.now()
        return current_day.month, current_day.year

    @staticmethod
    def create_lunch_days(month, year, lunch_users):
        if Lunchdate.objects.filter(date__year=year, date__month=month).count() < 28:
            num_days = calendar.monthrange(year, month)[1]
            days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
            objs = [Lunchdate(date=day) for day in days if day.weekday() != 5 and day.weekday() != 6
                    and not Lunchdate.objects.filter(date=day).count()]
            Lunchdate.objects.bulk_create(objs)
            now = datetime.datetime.now()
            if now.hour >= 10:
                lunch_days = Lunchdate.objects.filter(date__month=month, date__gt=now)
            else:
                lunch_days = Lunchdate.objects.filter(date__month=month, date__gte=now)
            lunch_objs = [Lunch(profile=user, date=day) for user in lunch_users for day in lunch_days
                          if user.lunch_weekly and day.date.weekday() in list(map(int, user.lunch_weekly.split(',')))
                          and not Lunch.objects.filter(profile=user, date=day).count()]
            Lunch.objects.bulk_create(lunch_objs)
            LunchService.update_lunar_month()

    @staticmethod
    def update_lunar_month():
        now = datetime.datetime.now()
        for date in Lunchdate.objects.filter(date__gte=now):
            solar = Solar(date.date.year, date.date.month, date.date.day)
            lunar = Converter.Solar2Lunar(solar)
            if lunar.day == 1 or lunar.day == 15:
                date.veggie = True
                date.save()

    @staticmethod
    def create_lunch_days_month(month, year, lunch_users):
        if Lunchdate.objects.filter(date__year=year, date__month=month).count() < 28:
            num_days = calendar.monthrange(year, month)[1]
            days = [datetime.date(year, month, day) for day in range(1, num_days + 1)]
            objs = [Lunchdate(date=day) for day in days if day.weekday() != 5 and day.weekday() != 6
                    and not Lunchdate.objects.filter(date=day).count()]
            Lunchdate.objects.bulk_create(objs)
            now = datetime.datetime.now()
            if now.hour >= 10:
                lunch_days = Lunchdate.objects.filter(date__month=month, date__gt=now)
            else:
                lunch_days = Lunchdate.objects.filter(date__month=month, date__gte=now)
            lunch_objs = [Lunch(profile=user, date=day) for user in lunch_users for day in lunch_days
                          if not Lunch.objects.filter(profile=user, date=day).count()]
            Lunch.objects.bulk_create(lunch_objs)

    @staticmethod
    def get_lunch_day_in_week(date):
        now = datetime.datetime.now()
        day = DateService.get_date(date)
        if day.date() < now.date() or (day.date() == now.date() and now.hour >= 10):
            days = [day + datetime.timedelta(days=i) for i in range(1, 6 - day.weekday() + 1)]
        else:
            days = [day + datetime.timedelta(days=i) for i in range(0, 6 - day.weekday() + 1)]
        return days

    @staticmethod
    def check_order_time(day, now):
        if day < now.date() or (day == now.date() and now.hour >= 10):
            raise ValidationError('Lunch order time is over.')
