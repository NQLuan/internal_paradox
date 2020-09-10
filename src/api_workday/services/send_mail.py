from django.template.loader import render_to_string

from api_base.services.sendmail import SendMail
from django.conf import settings


class SendMailRequestOff:

    @classmethod
    def send_request(cls, name_admin, name_user, list_email, date_off=None):
        date_off = cls.day_off(date_off)
        content = render_to_string('../templates/request_off.html',
                                   {'name_admin': name_admin, 'name_user': name_user, 'date_off': date_off})
        SendMail.start(list_email, 'Request off', content, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def send_forward_request(cls, name_admin, name_admin_manage, name_user, email, date_off=None):
        date_off = cls.day_off(date_off)
        content_user = render_to_string('../templates/forward_request_off.html',
                                        {'name_admin': name_admin, 'name_user': name_user,
                                         'name_admin_manage': name_admin_manage})

        content_manage = render_to_string('../templates/forward_request_off_to_manage.html',
                                          {'name_admin': name_admin, 'name_user': name_user,
                                           'name_admin_manage': name_admin_manage, 'date_off': date_off})
        SendMail.start(email['user'], 'Forward Request off', content_user)
        SendMail.start(email['admin'], 'Forward Request off', content_manage, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def send_reject_request(cls, name_user, name_admin, reason, list_email, date_off=None):
        content = render_to_string('../templates/reject_request_off.html',
                                   {'name_admin': name_admin, 'name_user': name_user,
                                    'reason': reason})
        SendMail.start(list_email, 'Reject request off', content, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def send_approve_request_to_user(cls, name_user, name_admin, list_email, date_off=None):
        date_off = cls.day_off(date_off)
        content = render_to_string('../templates/approve_request_off.html',
                                   {'name_admin': name_admin, 'name_user': name_user, 'date_off': date_off})
        SendMail.start(list_email, 'Approve Request off', content, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def send_approve_request_to_manage(cls, name_user, email_user, list_email, date_off=None):
        date_off = cls.day_off(date_off)
        content = render_to_string('../templates/leave_notice.html',
                                   {'name_user': name_user, 'email_user': email_user, 'date_off': date_off})
        SendMail.start(list_email, 'Approve Request off', content, cc=[settings.DEFAULT_EMAIL_ADMIN])

    @classmethod
    def day_off(cls, date_off):
        date_str = ''
        for date in date_off:
            date_str += '' + str(date.date) + ':' + str(date.type) + '\n'

        return date_str
