#!/usr/bin/env python

# author Huy
# date 9/19/2019

import datetime

from dateutil.relativedelta import relativedelta
from django.template.loader import render_to_string

from api.const import morning, afternoon, full
from api_base.services import BaseService, EmailThread, GoogleCalendar
from api_team.models import Team
from api_user.models import Profile
from api_workday.models import ProposeLeave, Lunch, Lunchdate, Date


class DateService(BaseService):

    @staticmethod
    def get_date(date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()

    @staticmethod
    def get_creation_data(data):
        proposed = ProposeLeave.objects.get(id=int(data.get('id')))
        proposed.status = 'Accepted'
        proposed.save()

        start_date = DateService.get_date(data.get('start'))
        end_date = DateService.get_date(data.get('end'))
        user = Profile.objects.get(id=data.get("profile"))

        content = render_to_string('../templates/accept_reject_email.html',
                                   {'user': user.name,
                                    'date': f'from {start_date} to {end_date} was ',
                                    'decision': 'accepted.',
                                    'further': ''})
        EmailThread(subject='Your leave day was accepted',
                    email=[user.user.email], content=content).start()

        if user.teams:
            user_team = Team.objects.get(id=int(user.teams.split(',')[0])).team_name
        else:
            user_team = 'No team'

        """Get weekdays, exclude Saturday and Sunday"""
        number_of_day = (end_date - start_date).days + 1
        f = lambda x: start_date + datetime.timedelta(days=x)
        dates = [f(i) for i in range(number_of_day) if f(i).weekday() != 5 and f(i).weekday() != 6]
        return dates, user.name, user_team, []

    @staticmethod
    def get_individual_data(data, user_name, date, dates):
        data['date'] = date
        start_time = data.get('start_hour')
        end_time = data.get('end_hour')
        start_hour = int(data.get('start_hour')[:2])
        end_hour = int(data.get('end_hour')[:2])
        if len(dates) == 1:
            data['content'] = f'{user_name} ({start_time} - {end_time})'
            data['type'] = {
                True: 'Morning',
                False: {
                    True: 'Afternoon',
                    False: 'Full day'
                }[start_hour >= 12]
            }[end_hour <= 13 and start_hour <= 13]
        else:
            if dates.index(date) == 0:
                data['content'] = f'{Profile.objects.get(id=data.get("profile")).name} ({start_time} - 17:30)'
                data['type'] = {
                    True: 'Full day',
                    False: 'Afternoon'
                }[start_hour < 12]
            elif dates.index(date) == len(dates) - 1:
                data['content'] = f'{Profile.objects.get(id=data.get("profile")).name} (08:00 - {end_time})'
                data['type'] = {
                    True: 'Full day',
                    False: 'Morning'
                }[end_hour > 13]
            else:
                data['content'] = f'{Profile.objects.get(id=data.get("profile")).name} (08:00 - 17:30)'
                data['type'] = 'Full day'
        return data

    @staticmethod
    def update_lunch(data, date):
        if data.get('lunch') == 'No' and Lunch.objects.filter(profile_id=int(data.get('profile')),
                                                              date__date=date).count():
            instance = Lunch.objects.get(profile_id=int(data.get('profile')), date__date=date)
            instance.delete()
        if data.get('lunch') == 'Yes' and not Lunch.objects.filter(profile_id=int(data.get('profile')),
                                                                   date__date=date).count():
            lunch_date = Lunchdate.objects.filter(date=date)
            if lunch_date.count():
                if not Lunch.objects.filter(profile_id=int(data.get('profile')), date=lunch_date[0]).count():
                    Lunch.objects.create(profile_id=int(data.get('profile')), date=lunch_date[0])
            else:
                lunch_date = Lunchdate.objects.create(date=date)
                Lunch.objects.create(profile_id=int(data.get('profile')), date=lunch_date)

    @staticmethod
    def duplicate_date(day, data, key, user_team):
        if day.type == key and data.get('type') != key:
            day.type = 'Full day'
            old_content = day.content
            new_content = {
                'Morning': f"{' '.join(data.get('content').split()[0:-3])} (8:00 - {data.get('end_hour')})",
                'Afternoon': f"{' '.join(data.get('content').split()[0:-3])} ({data.get('start_hour')} - 17:30)"
            }[key]
            day.content = new_content
            day.save()
            GoogleCalendar.update_event(data, old_content, new_content, user_team)

    @staticmethod
    def get_date_classes(serializer_data):
        for date in serializer_data:
            date['class'] = {
                morning: 'Morning',
                afternoon: 'Afternoon',
                full: 'Full'
            }[date['type']]
            date['start'] = date['end'] = date['date']
        return serializer_data

    @staticmethod
    def get_leave_day_statistic(profile_id):
        now = datetime.datetime.now()
        user_profile = Profile.objects.get(id=profile_id)

        last_year_queryset = Date.objects.filter(date__year=now.year - 1)
        last_remote, last_half_leave, last_full_leave = DateService.get_leave_remote(last_year_queryset, profile_id)
        last_total_leave = last_full_leave + last_half_leave * 0.5

        first_half_queryset = Date.objects.filter(date__year=now.year, date__month__lt=7)
        first_half_remote, first_half_half_leave, first_half_full_leave = DateService.get_leave_remote(
            first_half_queryset,
            profile_id)
        first_half_total_leave = first_half_full_leave + first_half_half_leave * 0.5

        last_leave_day_left = DateService.get_leave_day_in_year(last_total_leave, user_profile.join_date)
        if user_profile.join_date.month < 7:
            last_leave_day_left -= 1

        if now.month < 7:
            if last_leave_day_left > 0:
                current_leave_day_left = DateService.get_leave_day_in_year(first_half_total_leave,
                                                                           user_profile.join_date)
                leave_day_left = f"{last_leave_day_left} days last year, {current_leave_day_left} days this year"
            else:
                current_leave_day_left = DateService.get_leave_day_in_year(first_half_total_leave,
                                                                           user_profile.join_date) + last_leave_day_left
                leave_day_left = f"{current_leave_day_left} days"
            total_leave = DateService.convert_int(first_half_total_leave)
            total_remote = first_half_remote
        else:
            second_half_queryset = Date.objects.filter(date__year=now.year, date__month__gte=7)
            second_half_remote, second_half_half_leave, second_half_full_leave = DateService.get_leave_remote(
                second_half_queryset,
                profile_id)
            second_half_total_leave = second_half_full_leave + second_half_half_leave * 0.5
            if last_leave_day_left > 0:

                current_leave_day_left = DateService.get_leave_day_in_year(second_half_total_leave,
                                                                           user_profile.join_date)
            else:
                current_leave_day_left = DateService.get_leave_day_in_year(second_half_total_leave,
                                                                           user_profile.join_date) + last_leave_day_left
            leave_day_left = f"{current_leave_day_left} days"
            total_leave = DateService.convert_int(first_half_total_leave + second_half_total_leave)
            total_remote = first_half_remote + second_half_remote
        return {'id': profile_id,
                'name': user_profile.name,
                'leave_day_number': f'{total_leave} leave, {total_remote} remote',
                'leave_day_left': leave_day_left}

    @staticmethod
    def get_leave_remote(queryset, profile_id):
        remote = queryset.filter(profile_id=profile_id, title='Remote work').count()
        half_leave_day = queryset.filter(profile_id=profile_id, title='Leave').exclude(type='Full day').count()
        full_leave_day = queryset.filter(profile_id=profile_id, title='Leave', type='Full day').count()
        return remote, half_leave_day, full_leave_day

    @staticmethod
    def get_leave_day_in_year(total_leave, join_date):
        left = DateService.convert_int(12 - total_leave + relativedelta(datetime.datetime.now(), join_date).years)
        return left

    @staticmethod
    def convert_int(number):
        if number.is_integer():
            number = int(number)
        return number
