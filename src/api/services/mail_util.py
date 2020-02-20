#!/usr/bin/env python

# author Huy
# date 8/27/2019
from email.mime.base import MIMEBase

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.module_loading import import_string


class APIEmailMessage(EmailMessage):
    """
    Customize EmailMessage class to get mail username/password
    """

    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, cc=None,
                 reply_to=None, username=None, password=None, **kwargs):
        """
        Initialize a single email message (which can be sent to multiple
        recipients).
        """
        super().__init__(**kwargs)
        self.username = username
        self.password = password
        if to:
            if isinstance(to, str):
                raise TypeError('"to" argument must be a list or tuple')
            self.to = list(to)
        else:
            self.to = []
        if cc:
            if isinstance(cc, str):
                raise TypeError('"cc" argument must be a list or tuple')
            self.cc = list(cc)
        else:
            self.cc = []
        if bcc:
            if isinstance(bcc, str):
                raise TypeError('"bcc" argument must be a list or tuple')
            self.bcc = list(bcc)
        else:
            self.bcc = []
        if reply_to:
            if isinstance(reply_to, str):
                raise TypeError('"reply_to" argument must be a list or tuple')
            self.reply_to = list(reply_to)
        else:
            self.reply_to = []
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.subject = subject
        self.body = body or ''
        self.attachments = []
        if attachments:
            for attachment in attachments:
                if isinstance(attachment, MIMEBase):
                    self.attach(attachment)
                else:
                    self.attach(*attachment)
        self.extra_headers = headers or {}
        self.connection = connection

    def get_connection(self, backend=None, fail_silently=False, **kwds):
        if not self.connection:
            klass = import_string(backend or settings.EMAIL_BACKEND)
            self.connection = klass(fail_silently=fail_silently,
                                    username=self.username, password=self.password,
                                    **kwds)
        return self.connection
