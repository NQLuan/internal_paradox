import datetime

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api.models import Lunch
from api.models.profile import Profile
from api.serializers.profile_serializers import ProfileLunch, ProfileSerializers
from api.services import LunchService
from api.views import BaseViewSet


class ProfileViewSet(BaseViewSet):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializers
    pagination_class = None
    authentication_classes = (APIAuthentication,)
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'destroy': [IsAdminUser]}

    """
    LIST FUNCTION
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    """
    RETRIEVE FUNCTION
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data.copy()
        data['email'] = instance.user.email
        return Response(data)

    """
    UPDATE FUNCTIONS
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.data.get('email'):
            instance.user.email = request.data.get('email')
            instance.user.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def update_lunch(self, request, *args, **kwargs):
        data = request.data.copy()
        if data.get('lunch_weekly') == 'null':
            data['lunch_weekly'] = None
        data['lunch'] = {
            'true': True,
            'false': False
        }[data.get('check')]
        data['veggie'] = {
            'true': True,
            'false': False
        }[data.get('veggie')]
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ProfileLunch(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        now = datetime.datetime.now()
        Lunch.objects.filter(profile_id=instance.id, date__date__gt=datetime.datetime.now()).delete()
        LunchService.create_lunch_days(year=now.year, month=now.month, lunch_users=[instance])
        year, next_month = self.nextmonth(year=now.year, month=now.month)
        LunchService.create_lunch_days(year=year, month=next_month, lunch_users=[instance])
        return Response(data)

    @staticmethod
    def nextmonth(year, month):
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    """
    DELETE FUNCTION
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def get_profile_lunch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileLunch(instance)
        return Response(serializer.data)
