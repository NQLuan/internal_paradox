from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.authentications import APIAuthentication
from api.models import Profile, User
from api.serializers import InviteSerializer
from api.services import AdminService, ExcelImportService
from api.views import BaseViewSet


class AdminViewSet(BaseViewSet):
    authentication_classes = (APIAuthentication,)
    permission_classes = (IsAdminUser,)

    @action(methods=['post'], detail=False)
    def create_admin(self, request, *args, **kwargs):
        invite_serializer = InviteSerializer(data=request.data)
        invite_serializer.is_valid(raise_exception=True)
        user = User.objects.create_superuser(email=request.data['email'], password="123456")
        Profile.objects.create(user=user, name="Admin")
        return Response({"success": True})

    @action(methods=['post'], detail=False)
    def invite(self, request, *args, **kwargs):
        invite_serializer = InviteSerializer(data=request.data)
        invite_serializer.is_valid(raise_exception=True)
        return Response(AdminService.invite(request.data))

    @action(methods=['post'], detail=False)
    def send_first_row(self, request, *args, **kwargs):
        file = request.FILES['files'].file
        df, i = ExcelImportService.get_service(file)
        return Response({'columns': list(df.columns)})

    @action(methods=['post'], detail=False)
    def check_import(self, request, *args, **kwargs):
        file = request.FILES['files'].file
        df, import_service = ExcelImportService.get_service(file)
        rs = import_service.check_import(df=df, data=request.data)
        return Response(rs)

    @action(methods=['post'], detail=False)
    def import_file(self, request, *args, **kwargs):
        for row in request.data['rows']:
            if row['success']:
                AdminService.send_mail(email=row['email'], name=row['name'], phone=row['phone'])
        return Response({'success': True})
