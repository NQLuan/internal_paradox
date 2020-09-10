from django.db import transaction
from api_workday.models.request_off import RequestOff
from api_workday.models.request_detail import RequestDetail
from api_workday.serializers.request_off import RequestOffSerializer
from api_workday.serializers.action_request import RequestDetailSerializer
from api_workday.constants.date import Workday
from api_company.models import Company
from django.utils import timezone
from datetime import datetime
from api_workday.services.send_mail import SendMailRequestOff


class ActionRequestService:

    @classmethod
    def create_action_user(cls, request_off, profile):
        data = {
            "request_off": request_off.id,
            "approve": profile.id
        }

        serializer = RequestDetailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(request_off_id=request_off.id)

    @classmethod
    def action_approve(cls, request_off_id, user, comment):
        company_setting = Company.objects.filter().first()
        level = company_setting.maximum_level_approved
        user_action = RequestDetail.objects.filter(request_off_id=request_off_id)
        request_off = RequestOff.objects.filter(id=request_off_id).first()
        request_detail = RequestDetail.objects.filter(request_off_id=request_off_id, approve=user).first()
        if request_detail.status or request_off.status == Workday.STATUS_CANCEL:
            return request_detail
        with transaction.atomic():
            if request_off.status != Workday.STATUS_CANCEL:
                if user_action.count() < level and user.line_manager is not None:
                    request_off.status = Workday.STATUS_FORWARDED
                    request_off.save()
                    cls.create_action_user(request_off, user.line_manager)
                    email = {
                        'user': [request_off.profile.user.email],
                        'admin': [user.line_manager.user.email]
                    }
                    SendMailRequestOff.send_forward_request(name_admin=user.name,
                                                            name_admin_manage=user.line_manager.name,
                                                            name_user=request_off.profile.name, email=email,
                                                            date_off=request_off.date_off.all())
                else:
                    request_off.status = Workday.STATUS_APPROVED
                    request_off.save()

                    SendMailRequestOff.send_approve_request_to_user(name_admin=user.name, name_user=request_off.profile.name,
                                                            list_email=[request_off.profile.user.email], date_off=request_off.date_off.all())

                    list_email_manage = []
                    for manage in user_action:
                        list_email_manage.append(manage.approve.user.email)
                    SendMailRequestOff.send_approve_request_to_manage(name_user=request_off.profile.name,
                                                                      email_user=request_off.profile.user.email,
                                                                      list_email=list_email_manage,
                                                                      date_off=request_off.date_off.all())
            request_detail.status = Workday.STATUS_APPROVED
            request_detail.comment = comment
            request_detail.save()
        return request_detail

    @classmethod
    def action_reject(cls, request_off_id, user, comment):
        request_off = RequestOff.objects.filter(id=request_off_id).first()
        request_detail = RequestDetail.objects.filter(request_off_id=request_off_id, approve=user).first()
        if request_detail.status or request_off.status == Workday.STATUS_CANCEL:
            return request_detail
        with transaction.atomic():
            request_off.status = Workday.STATUS_REJECTED
            request_off.save()
            request_detail.status = Workday.STATUS_REJECTED
            request_detail.comment = comment
            request_detail.save()
            SendMailRequestOff.send_reject_request(name_user=request_off.profile.name, name_admin=user.name,
                                                   reason=request_detail.comment,
                                                   list_email=[request_off.profile.user.email])

        return request_detail

    @classmethod
    def action_cancel(cls, request_off_id, user):
        request_off = RequestOff.objects.filter(id=request_off_id, profile=user).first()
        date_off = request_off.date_off.all().order_by('-date').first()
        if cls.allow_or_not_cancel(date_off):
            if request_off.status == Workday.STATUS_CANCEL:
                return request_off
            request_off.status = Workday.STATUS_CANCEL
            request_off.save()

        return request_off

    @classmethod
    def allow_or_not_cancel(cls, date_off):
        if date_off.type in (Workday.MORNING, Workday.FULL):
            start_hour = str(date_off.date) + "T" + Workday.DEFAULT_START_HOUR + ":00+0700"
        else:
            start_hour = str(date_off.date) + "T" + Workday.DEFAULT_START_HOUR_AFTERNOON + ":00+0700"

        hour = datetime.strptime(start_hour, "%Y-%m-%dT%H:%M:%S%z") - timezone.now()
        if hour.days >= 0 and hour.seconds > 3600:
            return True
        return False
