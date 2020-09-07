from django.http import Http404

from api_workday.models.type_off import TypeOff
from api_workday.serializers.type_off import TypeOffSerizlizer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from api.authentications import APIAuthentication


class TypeOffView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, format=None):
        type_off = TypeOff.objects.all()
        serializer = TypeOffSerizlizer(type_off, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateTypeOffView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [APIAuthentication]

    def post(self, request, format=None):
        serializer = TypeOffSerizlizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditandDeleteTypeOffView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [APIAuthentication]

    def get_object(self, pk):
        try:
            return TypeOff.objects.get(pk=pk)
        except TypeOff.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        type_off = self.get_object(pk)
        serializer = TypeOffSerizlizer(type_off, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        type_off = self.get_object(pk)
        type_off.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
