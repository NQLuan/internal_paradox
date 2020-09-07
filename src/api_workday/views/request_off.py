from django.db import transaction
from django.http import Http404

from api_workday.models.request_off import RequestOff
from api_workday.models.date_off import DateOff
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.serializers.date_off import DateOffSerizlizer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api_workday.models.type_off import TypeOff
from rest_framework.response import Response
from rest_framework import status
from api.authentications import APIAuthentication
from api_workday.services.action_request import ActionRequestService
from rest_framework.generics import ListAPIView

from api_workday.services.request_off import RequestOffServices


class PostRequestOff(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [APIAuthentication]

    def post(self, request, format=None):

        data = request.data
        profile = request.user.profile
        type_off_id = request.data.get('type_id')
        type_off = TypeOff.objects.filter(id=type_off_id).first()

        # try:
        if RequestOffServices.check_date(data, DateOff):
            return Response({'error': 'There was a request for this date!'}, status=status.HTTP_400_BAD_REQUEST)
        request_data = {"reason": data["reason"]}
        requestSerializer = RequestOffSerializer(data=request_data)
        with transaction.atomic():
            if requestSerializer.is_valid():
                requestSerializer.save(type_off=type_off, profile=profile)
            request_id = requestSerializer.data['id']
            for date in data["date"]:
                date_data = {
                    "date": date["date"],
                    "type": date["type"],
                    "lunch": date["lunch"],
                    "request_off": request_id
                }
                dateSerializer = DateOffSerizlizer(data=date_data)
                if dateSerializer.is_valid(raise_exception=True):
                    dateSerializer.save()
            ActionRequestService.create_action_user(request_id, profile.line_manager.id)
            return Response(requestSerializer.data, status=status.HTTP_201_CREATED)
        # except:
        #     return Response(requestSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestOffDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [APIAuthentication]

    def get_object(self, pk):
        try:
            return RequestOff.objects.get(pk=pk)
        except RequestOff.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        request_off = self.get_object(pk)
        serializer = RequestOffSerializer(request_off)
        return Response(serializer.data)


class EditOrDeleteRequestOff(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [APIAuthentication]

    def get_object(self, pk):
        try:
            return RequestOff.objects.get(pk=pk)
        except RequestOff.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        request_off = self.get_object(pk)
        serializer = RequestOffSerializer(request_off, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        request_off = self.get_object(pk)
        request_off.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetMyRequest(ListAPIView):
    queryset = RequestOff.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [APIAuthentication]
    serializer_class = RequestOffSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        return self.queryset.filter(profile=profile).order_by('-created_at')
