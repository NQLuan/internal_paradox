#!/usr/bin/env python

# author Huy
# date 12/8/2019

import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from prompt_toolkit.validation import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api_base.services import TokenUtil, EmailThread, Utils
from api_user.models import User, Profile
from api_workday.models import Lunch, Date
from api_workday.services import LunchService


class ActionViewSet(viewsets.ViewSet):
    @action(methods=['post'], detail=False)
    def forgot_password(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get('email'))
            token = TokenUtil.encode(user)
            link = f'http://{settings.API_HOST}/resetPassword?token={token}'
        except:
            raise ValidationError(message='User does not exist')

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
        current_month, current_year = Utils.get_current_date()
        LunchService.create_lunch_days(current_month, current_year, lunch_users=Profile.objects.filter(lunch=True))
        return Response({'success': True})

