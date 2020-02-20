#!/usr/bin/env python

# author Huy
# date 12/8/2019
import calendar
import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from prompt_toolkit.validation import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Date, Lunch, Profile, User
from api.services import EmailThread, LunchService, TokenUtil


# from chatbot import TestRun


class ActionViewSet(viewsets.ViewSet):
    @action(methods=['post'], detail=False)
    def forgot_password(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get('email'))
            token = TokenUtil.encode(user)
            link = f'http://35.209.247.237/resetPassword?token={token}'
        except:
            raise ValidationError('User does not exist')

        content = render_to_string('../templates/password_email.html', {'link': link})

        EmailThread(subject='Forgot Password', email=[request.data.get('email')], content=content).start()
        return Response({"success": True})

    @action(methods=['put'], detail=False)
    def change_password(self, request, *args, **kwargs):
        user = TokenUtil.decode(request.data.get('token'), 1)
        user.password = make_password(request.data.get('password'), salt=settings.SECRET_KEY)
        user.save()
        return Response({"success": True})

    @action(methods=['post'], detail=False)
    def create_lunch_current_month(self, request, *args, **kwargs):
        current_month, current_year = LunchService.get_current_date()
        LunchService.create_lunch_days(current_month, current_year, lunch_users=Profile.objects.filter(lunch=True))
        return Response({'success': True})

    @action(methods=['post'], detail=False)
    def create_lunch_next_month(self, request, *args, **kwargs):
        current_month, current_year = LunchService.get_current_date()
        year, next_month = calendar.nextmonth(year=current_year, month=current_month)
        LunchService.create_lunch_days(next_month, year, lunch_users=Profile.objects.filter(lunch=True))
        return Response({'success': True})

    @action(methods=['get'], detail=False)
    def get_lunch(self, request, *args, **kwargs):
        return Response(Lunch.objects.filter(date__date=datetime.datetime.now().date()).count())

    @action(methods=['get'], detail=False)
    def get_leave(self, request, *args, **kwargs):
        leave = Date.objects.filter(date=datetime.datetime.now(), title='Leave')
        leave_profiles = [date.profile_id for date in leave]
        leave_names = [profile.name for profile in Profile.objects.filter(id__in=leave_profiles)]
        leave_text = '\n• '.join(leave_names)

        remote = Date.objects.filter(date=datetime.datetime.now(), title='Remote work')
        remote_profiles = [date.profile_id for date in remote]
        remote_names = [profile.name for profile in Profile.objects.filter(id__in=remote_profiles)]
        remote_text = '\n• '.join(remote_names)

        if len(leave_names) == 0:
            if len(remote_names) == 0:
                text = 'No one leave today'
            else:
                text = f'There is *_{len(remote_names)}_* people working remote today:\n ```• {remote_text}```'
        else:
            if len(remote_names) == 0:
                text = f'There is *_{len(leave_names)}_* people leave today:\n```• {leave_text}```'
            else:
                text = f'There is *_{len(leave_names)}_* people leave today:\n```• {leave_text}```\n' \
                       f'And *_{len(remote_names)}_* people working remote today:\n```• {remote_text}```'
        return Response(text)

    # @action(methods=['post'], detail=False)
    # def chatbot(self, request, *args, **kwargs):
    #     response = TestRun.run_api_dialogue(request.data.get('text'))
    #     if response == ' adjust_lunch_stt':
    #         if Lunch.objects.filter(profile=int(request.data.get('id')), date__date=datetime.datetime.now()).count():
    #             response = 'You have lunch today'
    #         else:
    #             response = 'You do not have lunch today'
    #     elif response.split('_')[0].strip() == 'Leave' or response.split('_')[0].strip() == 'Remote':
    #         ProposeLeave.objects.create(start=datetime.datetime.strptime(response.split('_')[2], '%d - %m - %Y'),
    #                                     end=datetime.datetime.strptime(response.split('_')[4], '%d - %m - %Y'),
    #                                     lunch='No', title=response.split('_')[0].strip(),
    #                                     profile=Profile.objects.get(id=int(request.data.get('id'))))
    #         if response.split('_')[2] == response.split('_')[4]:
    #             response = f"Done! Your leave for day {response.split('_')[2].replace(' ', '')} is proposed. You can check the website to see if I have made a mistake."
    #         else:
    #             response = f"Done! Your leave from {response.split('_')[2].replace(' ', '')} to {response.split('_')[4].replace(' ', '')} is proposed. You can check the website to see if I have made a mistake."
    #     elif response == ' msg_ask_self_name':
    #         name = Profile.objects.get(id=int(request.data.get('id'))).name
    #         response = f"Your name is {name}. What a lovely name! :)"
    #     return Response({'text': response})
