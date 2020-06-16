#!/usr/bin/env python

# author Huy
# date 10/23/2019

import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api_base.views import BaseViewSet
from api_user.models import Profile
from api_user.serializers import ProfileName
from api_workday.models import Lunch, Lunchdate
from api_workday.serializers import LunchSerializer
from api_workday.services import LunchService, DateService


class LunchViewSet(BaseViewSet):
    queryset = Lunch.objects.all()
    serializer_class = LunchSerializer
    pagination_class = None
    authentication_classes = (APIAuthentication,)
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {'list': [IsAdminUser], 'get_lunch_status': [IsAdminUser]}

    def lunch_creation(self, request, day):
        LunchService.check_order_time(day, datetime.datetime.now())
        if not Lunchdate.objects.filter(date=day).count():
            Lunchdate.objects.create(date=day)
        data = request.data.copy()
        data['date'] = Lunchdate.objects.get(date=day).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return serializer

    def create(self, request, *args, **kwargs):
        day = DateService.get_date(request.data.get('date'))
        serializer = self.lunch_creation(request, day)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def update_lunch_user(self, request, *args, **kwargs):
        day = DateService.get_date(request.data.get('date'))
        if Lunchdate.objects.filter(date=day).count():
            lunch_date = Lunchdate.objects.get(date=day)
            if Lunch.objects.filter(profile=kwargs.get('pk'), date=lunch_date).count():
                instance = Lunch.objects.get(profile=kwargs.get('pk'), date=lunch_date)
                LunchService.check_order_time(instance.date.date, datetime.datetime.now())
                self.perform_destroy(instance)
                stt = status.HTTP_204_NO_CONTENT
                rs = 'Removed successfully'
            else:
                self.lunch_creation(request, day)
                stt = status.HTTP_201_CREATED
                rs = 'Created successfully'
        else:
            self.lunch_creation(request, day)
            stt = status.HTTP_201_CREATED
            rs = 'Created successfully'
        return Response({'response': rs}, status=stt)

    def list(self, request, *args, **kwargs):
        response = []
        now = datetime.datetime.now()
        next_year, next_month = self.nextmonth(year=now.year, month=now.month)
        for date in Lunchdate.objects.filter(date__month__in=[now.month, next_month]):
            queryset = self.filter_queryset(self.get_queryset()).filter(date=date.id).values('profile')
            for data in queryset:
                data['name'] = Profile.objects.get(id=data.get('profile')).name
            profiles = Profile.objects.filter(user__active=True).exclude(
                id__in=[data.get('profile') for data in queryset]).values('id', 'name')
            response.extend(({'start': date.date, 'end': date.date, 'title': 'Eat', 'class': 'eat',
                              'content': str(queryset.count()), 'reason': queryset},
                             {'start': date.date, 'end': date.date, 'title': 'No eat', 'class': 'no',
                              'content': str(profiles.count()), 'reason': profiles}))
        return Response(response)

    @staticmethod
    def nextmonth(year, month):
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(profile_id=kwargs.get('pk'))
        serializer = self.get_serializer(queryset, many=True)
        for data in serializer.data:
            data['start'] = data['end'] = Lunchdate.objects.get(id=data.get('date')).date
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        instance = self.get_object()
        day = instance.date.date
        LunchService.check_order_time(day, now)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def get_lunch_status(self, request, *args, **kwargs):
        day = DateService.get_date(request.query_params.get('date'))
        profiles = list(lunch.profile_id for lunch in Lunch.objects.filter(date__date=day))
        queryset = Profile.objects.select_related('user').filter(user__active=True).values('id', 'name')
        serializer = ProfileName(queryset, many=True)
        for data in serializer.data:
            if data.get('id') in profiles:
                data['lunch_id'] = Lunch.objects.get(date__date=day, profile_id=data.get('id')).id
                data['status'] = 'Lunch'
            else:
                data['status'] = 'No lunch'
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def retrieve_lunch_status(self, request, *args, **kwargs):
        day = DateService.get_date(request.query_params.get('date'))
        instance = Profile.objects.get(id=int(kwargs.get('pk')))
        serializer = ProfileName(instance)
        data = serializer.data.copy()
        lunch = Lunch.objects.filter(date__date=day, profile_id=instance.id)
        if lunch.count():
            data['lunch_id'] = lunch[0].id
            data['status'] = 'Lunch'
        else:
            data['status'] = 'No lunch'
        return Response([data])

    @action(methods=['post'], detail=True)
    def create_user_lunch_month(self, request, *args, **kwargs):
        day = DateService.get_date(request.data.get('date'))
        LunchService.create_lunch_days_month(year=day.year, month=day.month,
                                             lunch_users=Profile.objects.filter(id=kwargs.get('pk')))
        return Response({'success': True})

    @action(methods=['delete'], detail=True)
    def remove_user_lunch_month(self, request, *args, **kwargs):
        day = DateService.get_date(request.data.get('date'))
        lunch_days = [date.id for date in Lunchdate.objects.filter(date__month=day.month, date__year=day.year)]
        Lunch.objects.filter(profile=int(kwargs.get('pk')), date__in=lunch_days).delete()
        return Response({'success': True})

    @action(methods=['post'], detail=True)
    def update_user_lunch_by_days(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        start_date = DateService.get_date(request.data.get('start_date'))
        end_date = DateService.get_date(request.data.get('end_date'))
        number_of_day = (end_date - start_date).days + 1
        f = lambda x: start_date + datetime.timedelta(days=x)
        if now.hour >= 10:
            dates = [f(i) for i in range(number_of_day) if
                     f(i).weekday() != 5 and f(i).weekday() != 6 and f(i) > now.date()]
        else:
            dates = [f(i) for i in range(number_of_day) if
                     f(i).weekday() != 5 and f(i).weekday() != 6 and f(i) >= now.date()]
        if request.data.get('type') == 'Remove':
            Lunch.objects.filter(profile=int(kwargs.get('pk')), date__date__in=dates).delete()
        else:
            lunch_objs = [Lunch(profile=Profile.objects.get(id=kwargs.get('pk')), date=Lunchdate.objects.get(date=day))
                          for day in dates if not Lunch.objects.filter(profile=int(kwargs.get('pk')), date__date=day)]
            Lunch.objects.bulk_create(lunch_objs)
        return Response({'success': True})
