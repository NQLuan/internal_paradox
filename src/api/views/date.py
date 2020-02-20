#!/usr/bin/env python

# author Huy
# date 9/7/2019
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api.models import Date, Profile
from api.serializers import DateSerializer
from api.services import DateService, GoogleCalendar
from api.views import BaseViewSet


class DateViewSet(BaseViewSet):
    queryset = Date.objects.filter(date__year=datetime.now().year)
    serializer_class = DateSerializer
    pagination_class = None
    authentication_classes = (APIAuthentication,)
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {'create': [IsAdminUser], 'list_date_statistic': [IsAdminUser]}

    def create(self, request, *args, **kwargs):
        dates, user_name, user_team, rs = DateService.get_creation_data(request.data)
        for date in dates:
            data = DateService.get_individual_data(request.data.copy(), user_name, date, dates)
            if self.queryset.filter(date=date, profile_id=request.data.get('profile')).count():
                existed_date = Date.objects.get(date=date, profile_id=request.data.get('profile'))
                DateService.duplicate_date(existed_date, data, 'Morning', user_team)
                DateService.duplicate_date(existed_date, data, 'Afternoon', user_team)
                continue
            else:
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                GoogleCalendar.create_event(data, user_team)
                DateService.update_lunch(data, date)
                rs.append(serializer.data)
        leave_date_left = DateService.get_leave_day_statistic(request.data.get('profile')).get('leave_day_left')
        return Response({'success': True, 'result': rs, 'leave_day_left': leave_date_left},
                        status=status.HTTP_201_CREATED)

    """
    LIST FUNCTION
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = DateService.get_date_classes(serializer.data)
        return Response(data)

    """
    RETRIEVE FUNCTION
    """

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(profile_id=kwargs.get('pk'))
        serializer = self.get_serializer(queryset, many=True)
        data = DateService.get_date_classes(serializer.data)
        return Response(data)

    @action(methods=['get'], detail=False)
    def list_date_statistic(self, request, *args, **kwargs):
        rs = list((DateService.get_leave_day_statistic(profile.id) for profile in Profile.objects.filter(
            user__active=True)))
        return Response(rs)

    @action(methods=['get'], detail=True)
    def retrieve_date_statistic(self, request, *args, **kwargs):
        return Response(DateService.get_leave_day_statistic(kwargs.get('pk')))

    @action(methods=['get'], detail=False)
    def get_today(self, request, *args, **kwargs):
        leave = Date.objects.filter(date=datetime.now(), title='Leave').count()
        remote = Date.objects.filter(date=datetime.now(), title='Remote work').count()
        return Response({'leave': leave,
                         'remote': remote})
