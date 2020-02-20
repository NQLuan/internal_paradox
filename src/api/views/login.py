#!/usr/bin/env python

# author Huy
# date 8/14/2019

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import InviteSerializer, LoginSerializer
from api.services import LoginService, TokenUtil


class LoginViewSet(viewsets.ViewSet):
    activity_log = True

    @staticmethod
    def create(request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        validated_data = login_serializer.validated_data
        rs = LoginService.login(validated_data)
        return Response(rs)

    @action(methods=['post'], detail=False)
    def verify(self, request, *args, **kwargs):
        data = TokenUtil.verify(request.data.get('token'))
        invite_serializer = InviteSerializer(data=data)
        invite_serializer.is_valid(raise_exception=True)
        LoginService.verify(data, request.data.get('password'))
        return Response({'success': True})
