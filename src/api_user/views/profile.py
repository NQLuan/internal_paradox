from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api_base.views import BaseViewSet
from api_user.models.profile import Profile
from api_user.serializers import ProfileLunch, ProfileSerializers
from api_workday.services import LunchService


class ProfileViewSet(BaseViewSet):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializers
    pagination_class = None
    authentication_classes = (APIAuthentication,)
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'destroy': [IsAdminUser]}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.email = instance.user.email
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
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
        # TODO Create a service/update validate for ProfileLunch for this
        data = request.data.copy()
        if data.get('lunch_weekly') == 'null':
            data['lunch_weekly'] = None
        # TODO Check UI again for this
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

        LunchService.update_lunch(instance)

        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def get_profile_lunch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProfileLunch(instance)
        return Response(serializer.data)
