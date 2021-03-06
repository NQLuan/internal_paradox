from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response

from api_admin.services import ExcelImportService
from api_base.serializers import InviteSerializer
from api_base.views import BaseViewSet
from api_user.models import User, Profile
from api_user.services import UserService


class AdminViewSet(BaseViewSet):

    @action(methods=['post'], detail=False)
    def create_admin(self, request, *args, **kwargs):
        secret_key = request.data.get('secret_key')
        if secret_key == settings.SECRET_KEY:
            invite_serializer = InviteSerializer(data=request.data)
            invite_serializer.is_valid(raise_exception=True)
            user = User.objects.create_superuser(email=request.data.get('email'), password="123456")
            Profile.objects.create(user=user, name="Admin")
            return Response({"success": True})
        return Response({"success": False})

    # TODO Update UI to use new endpoint
    @action(methods=['post'], detail=False)
    def invite(self, request, *args, **kwargs):
        invite_serializer = InviteSerializer(data=request.data)
        invite_serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        name = request.data.get('name')
        res = UserService.invite(email, name)
        return Response(res)

    # TODO Move these 3 to separate view
    @action(methods=['post'], detail=False)
    def send_first_row(self, request, *args, **kwargs):
        file = request.FILES.get('files').file
        df = ExcelImportService.read_excel(file)
        return Response({'columns': list(df.columns)})

    @action(methods=['post'], detail=False)
    def check_import(self, request, *args, **kwargs):
        file = request.FILES.get('files').file
        import_service = ExcelImportService()
        df = import_service.read_excel(file)
        rs = import_service.check_import(df=df, data=request.data)
        return Response(rs)

    @action(methods=['post'], detail=False)
    def import_file(self, request, *args, **kwargs):
        for row in request.data.get('rows'):
            if row.get('success'):
                UserService.send_mail(email=row.get('email'), name=row.get('name'), phone=row.get('phone'))
        return Response({'success': True})
