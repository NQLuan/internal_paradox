#!/usr/bin/env python

import datetime
# author Huy
# date 11/26/2019
import json

from django.template.loader import render_to_string
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api.models import Date, Profile, ProposeLeave, Team, User
from api.serializers import ProposeLeaveSerializer
from api.services import DateService, EmailThread, GoogleCalendar
from api.views import BaseViewSet


class ProposeLeaveViewSet(BaseViewSet):
    queryset = ProposeLeave.objects.all()
    serializer_class = ProposeLeaveSerializer
    pagination_class = None
    authentication_classes = (APIAuthentication,)
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'reject': [IsAdminUser]}

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = Profile.objects.get(id=int(request.data.get('profile')))
        content = render_to_string('../templates/admin_leave_email.html',
                                   {'user': user.name,
                                    'date': f'from {request.data.get("start")} to {request.data.get("end")}'})
        EmailThread(subject='A new leave from users is proposed',
                    email=[user.email for user in User.objects.filter(admin=True)], content=content).start()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = ProposeLeave.objects.filter(start__gte=datetime.datetime.now())
        if request.query_params.get('history'):
            queryset = ProposeLeave.objects.all()
        data = self.get_data(queryset, request.query_params.get('history'))
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        queryset = ProposeLeave.objects.filter(start__gte=datetime.datetime.now(), profile=kwargs.get('pk'))
        if request.query_params.get('history'):
            queryset = ProposeLeave.objects.filter(start__lt=datetime.datetime.now(), profile=kwargs.get('pk'))
        data = self.get_data(queryset, request.query_params.get('history'))
        return Response(data)

    def get_data(self, queryset, history):
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            profile = Profile.objects.get(id=data.get('profile'))
            data['name'] = profile.name
            data['leave_day_left'] = DateService.get_leave_day_statistic(data.get('profile')).get('leave_day_left')
            data['team'] = Team.objects.get(id=int(profile.teams.split(',')[0])).team_name
            data['leave_day_left'] = DateService.get_leave_day_statistic(data.get('profile')).get('leave_day_left')
            if data.get('start_hour') and data.get('end_hour'):
                start_hour_json = json.loads(data.get('start_hour'))
                end_hour_json = json.loads(data.get('end_hour'))
                data['start_hour'] = f"{start_hour_json.get('hour')}:{start_hour_json.get('min')}"
                data['end_hour'] = f"{end_hour_json.get('hour')}:{end_hour_json.get('min')}"
            else:
                data['start_hour'] = '08:00'
                data['end_hour'] = '17:30'
            if history and data.get('status') == 'Pending':
                data['status'] = 'Passed'
        return serializer.data

    @action(methods=['put'], detail=True)
    def reject(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = 'Rejected'
        instance.comments = request.data.get('comments')
        instance.save()

        user = Profile.objects.get(id=instance.profile_id)
        reason = ''
        if request.data.get('comments'):
            reason = f"Reason: {request.data.get('comments')}."
        content = render_to_string('../templates/accept_reject_email.html',
                                   {'user': user.name,
                                    'date': f'from {instance.start} to {instance.end} was ',
                                    'decision': 'rejected. ',
                                    'further': reason})
        EmailThread(subject='Your leave day was rejected',
                    email=[user.user.email], content=content).start()

        return Response({'success': True})

    @action(methods=['put'], detail=True)
    def withdraw(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == 'Accepted':
            number_of_day = (instance.end - instance.start).days + 1
            f = lambda x: instance.start + datetime.timedelta(days=x)
            dates = [f(i) for i in range(number_of_day) if f(i).weekday() != 5 and f(i).weekday() != 6]
            date_objects = Date.objects.filter(profile_id=instance.profile, date__in=dates)

            user = Profile.objects.get(id=instance.profile_id)
            if user.teams:
                user_team = Team.objects.get(id=int(user.teams.split(',')[0])).team_name
            else:
                user_team = 'No team'
            items = GoogleCalendar.get()
            GoogleCalendar.delete_event(items, date_objects, user_team)
            date_objects.delete()
        self.perform_destroy(instance)
        return Response({'success': True})

    @action(methods=['get'], detail=False)
    def get_new_leave(self, request, *args, **kwargs):
        count = ProposeLeave.objects.filter(start__gte=datetime.datetime.now(), status='Pending').count()
        return Response({'number': count})
