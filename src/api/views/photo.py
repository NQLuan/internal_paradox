#!/usr/bin/env python

# author Huy
# date 9/18/2019
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api.models import Photo
from api.serializers import PhotoSerializer
from api.views import BaseViewSet


class PhotoViewSet(BaseViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    pagination_class = None
    authentication_classes = (APIAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        rs = []
        data = request.data.copy()
        for image in data.getlist('image'):
            data['photo'] = image
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            rs.append(serializer.data)
        return Response(rs, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        filter_kwargs = kwargs['pk']
        queryset = self.filter_queryset(self.get_queryset()).filter(profile=filter_kwargs)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)