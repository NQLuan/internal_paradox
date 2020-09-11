from rest_framework.views import APIView
from api_workday.services.action_request import ActionRequestService
from api_workday.constants import Workday
from api_workday.serializers.action_request import RequestDetailSerializer
from rest_framework.response import Response
from rest_framework import status
from api.authentications import APIAuthentication
from rest_framework.permissions import IsAuthenticated
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.models.request_detail import RequestDetail
from rest_framework.pagination import PageNumberPagination
# from api.pagination import CustomPagination
from datetime import date
from api_workday.models.date_off import DateOff
import pytz
from rest_framework.generics import ListAPIView


class ActionRequest(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [APIAuthentication]
    pagination_class = PageNumberPagination

    def post(self, request, format=None):
        action = request.data.get('action')
        request_off_id = request.data.get('request_off_id')
        comment = request.data.get('comment')
        user = request.user.profile
        try:
            if action == Workday.STATUS_APPROVED:
                data = ActionRequestService.action_approve(request_off_id, user, comment)
                serializer = RequestDetailSerializer(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif action == Workday.STATUS_REJECTED:
                data = ActionRequestService.action_reject(request_off_id, user, comment)
                serializer = RequestDetailSerializer(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif action == Workday.STATUS_CANCEL:
                data = ActionRequestService.action_cancel(request_off_id, user)
                serializer = RequestOffSerializer(data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetRequestDetail(ListAPIView):
    queryset = RequestDetail.objects.all()
    authentication_classes = [APIAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None
    serializer_class = RequestDetailSerializer

    def get_queryset(self):
        profile = self.request.user.profile
        queryset = self.queryset.filter(approve=profile).order_by('-created_at')
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        if year:
            date_off = DateOff.objects.filter(date__year=year)
            queryset = queryset.filter(request_off__date_off__in=date_off)
            if month:
                date_off = date_off.filter(date__month=month)
                queryset = queryset.filter(request_off__date_off__in=date_off)
                if day:
                    date_off = date_off.filter(date__day=day)
                    queryset = queryset.filter(request_off__date_off__in=date_off)
        return queryset
