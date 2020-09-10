from django.http import Http404

from api_company.models import Company
from api_company.serializers import CompanySerizlizer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from api.authentications import APIAuthentication


class CompanyView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, format=None):
        company = Company.objects.all()
        serializer = CompanySerizlizer(company, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateCompanyView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [APIAuthentication]

    def post(self, request, format=None):
        serializer = CompanySerizlizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditandDeleteCompanyView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [APIAuthentication]

    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        company = self.get_object(pk)
        serializer = CompanySerizlizer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        company = self.get_object(pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
