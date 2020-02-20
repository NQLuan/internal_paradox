#!/usr/bin/env python

# author Huy 
# date 8/19/2019

import threading

from django.conf import settings

from api.services import APIEmailMessage


class EmailThread(threading.Thread):
    def __init__(self, subject=None, content=None, email=None, sender=None, email_password=None):
        self.subject = subject
        self.content = content
        self.sender = sender or settings.EMAIL_HOST_USER
        self.mail_password = email_password or settings.EMAIL_HOST_PASSWORD
        self.recipient_list = email
        threading.Thread.__init__(self)

    def run(self):
        msg = APIEmailMessage(subject=self.subject, body=self.content, from_email=self.sender,
                              to=self.recipient_list, cc=None, bcc=None,
                              username=self.sender, password=self.mail_password)
        msg.content_subtype = 'html'
        msg.send()
