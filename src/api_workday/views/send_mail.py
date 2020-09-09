from django.core.mail import EmailMessage, send_mail
from django.core import mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from api_base.services.sendmail import SendMail

class SendMailToUser(APIView):
    def post(self, request):
        content = "Hello world"
        SendMail.start(['nguyenquangluan02@gmail.com'], cc=['nguyenquangluan1@gmail.com'], bcc=['do.nguyen.tt.1995@gmail.com'], subject='Subject here', content=content)
        return Response(status=status.HTTP_200_OK)

