from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api_base.serializers import InviteSerializer
from api_base.services import Utils
from api_base.views import BaseViewSet
from api_user.models import User
from api_user.serializers import UserSerializer
from api_user.services import UserService


class UserViewSet(BaseViewSet):
    queryset = User.objects.select_related('profile')
    serializer_class = UserSerializer
    authentication_classes = (APIAuthentication,)
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {'activate': [IsAdminUser], 'destroy': [IsAdminUser], 'create': [IsAdminUser]}

    def create(self, request, *args, **kwargs):
        invite_serializer = InviteSerializer(data=request.data)
        invite_serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        name = request.data.get('name')
        res = UserService.invite(email, name)
        return Response(res)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        active = self.request.query_params.get('active')
        if active:
            queryset = queryset.filter(Q(active=1 and Utils.convert_to_int(active)))
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        return self.get_paginated_response(data)

    @action(methods=['get'], detail=False)
    def get_non_paginate(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(active=True)
        data = self.get_serializer(queryset, many=True).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.get_serializer(instance).data
        return Response(data)

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

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        UserService.deactivate_user(user)
        return Response({"Success": True}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def activate(self, request, *args, **kwargs):
        user = self.get_object()
        UserService.activate_user(user)
        return Response({"Success": True})

    @action(methods=['put'], detail=True)
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        user = UserService.update_password(request.data, user)
        if user:
            self.perform_update(user)
            return Response({"Success": True})
        return Response({"Success": False})
