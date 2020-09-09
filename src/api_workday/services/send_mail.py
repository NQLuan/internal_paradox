from django.template.loader import render_to_string

from api_base.services.sendmail import SendMail
from django.conf import settings


class SendMailRequestOff:

    @classmethod
    def send_request(cls, name_admin, name_user, date_off, list_email):
        content = render_to_string('../templates/request_off.html',
                                   {'name_admin': name_admin, 'name_user': name_user})
        SendMail.start(list_email, 'Request off', content, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def send_forward_request(cls, name_admin, name_admin_manage, name_user, date_off, email):
        content_user = render_to_string('../templates/forward_request_off.html',
                                        {'name_admin': name_admin, 'name_user': name_user,
                                         'name_admin_manage': name_admin_manage})

        content_manage = render_to_string('../templates/forward_request_off_to_manage.html',
                                          {'name_admin': name_admin, 'name_user': name_user,
                                           'name_admin_manage': name_admin_manage})
        SendMail.start(email.user, 'Forward Request off', content_user, cc=[settings.DEFAULT_EMAIL_ADMIN])
        SendMail.start(email.admin, 'Forward Request off', content_manage, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def send_reject_request(cls, name_user, name_admin, reason, list_email):
        content = render_to_string('../templates/reject_request_off.html',
                                   {'name_admin': name_admin, 'name_user': name_user,
                                    'reason': reason})
        SendMail.start(list_email, 'Reject request off', content, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def send_approve_request(cls, name_user, name_admin, list_email):
        content = render_to_string('../templates/forward_request_off.html',
                                   {'name_admin': name_admin, 'name_user': name_user})
        SendMail.start(list_email, 'Approve Request off', content, cc=[settings.DEFAULT_EMAIL_ADMIN])
