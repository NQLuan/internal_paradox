from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api.models import User
from api.serializers import UserSerializer
from api.services import UserService
from api.views import BaseViewSet


class UserViewSet(BaseViewSet):
    queryset = User.objects.select_related('profile')
    serializer_class = UserSerializer
    authentication_classes = (APIAuthentication,)
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'activate': [IsAdminUser], 'destroy': [IsAdminUser]}

    def create(self, request, *args, **kwargs):
        raise NotImplementedError('Create must be implemented')

    """
    LIST FUNCTION
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        active = self.request.query_params.get('active')
        if active:
            queryset = queryset.filter(Q(active=1 and UserService.convert_to_int(active)))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = UserService.get_team(users=serializer.data)
        return self.get_paginated_response(data)

    @action(methods=['get'], detail=False)
    def get_non_paginate(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(active=True)
        serializer = self.get_serializer(queryset, many=True)
        data = UserService.get_team(users=serializer.data)
        return Response(data)

    """
    RETRIEVE FUNCTION
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = UserService.get_photo(data=serializer.data.copy())
        return Response(data)

    """
    UPDATE FUNCTION
    """

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

    """
    DE-ACTIVATE EMPLOYEE FUNCTION
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        instance.profile.teams = None
        instance.profile.save()
        return Response({"Success": True}, status=status.HTTP_204_NO_CONTENT)

    """
    ACTIVATE EMPLOYEE FUNCTION
    """

    @action(methods=['put'], detail=True)
    def activate(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = True
        instance.save()
        return Response({"Success": True})

    """
    CHANGE PASSWORD FUNCTION
    """

    @action(methods=['put'], detail=True)
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        self.update_password(data=request.data, instance=instance)
        return Response({"Success": True})

    def update_password(self, data, instance):
        if data.get('current_password') is not None and data.get('current_password') != "" \
                and not instance.password == make_password(password=data.get('current_password'),
                                                           salt=settings.SECRET_KEY):
            raise ValidationError("Error: Password does not match")
        instance.set_password(data.get('new_password'))
        self.perform_update(instance)
