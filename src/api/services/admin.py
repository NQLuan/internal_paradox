#!/usr/bin/env python

# author OS
# date 7/24/2019
import datetime

from django.template.loader import render_to_string

from api.models import Profile, User
from api.services import BaseService, EmailThread, TokenUtil


class AdminService(BaseService):
    """
    INVITE METHOD
    """

    @staticmethod
    def invite(data):
        email = data['email']
        name = data['name']
        AdminService.send_mail(sender=None, email=email, name=name, phone="")
        return {
            "success": True,
            "user": {
                'name': name,
                'email': email
            }
        }

    @staticmethod
    def send_mail(sender=None, email=None, name=None, phone=None, personal_email=None):
        token = TokenUtil.verification_encode(name, email, phone, personal_email)
        link = f'https://35.209.247.237/verify?token={token}'
        content = render_to_string('../templates/invitation_email.html',
                                   {'name': name, 'email': email, 'link': link, 'token': token})
        EmailThread(subject='Welcome to Company Management',
                    email=[email, personal_email], sender=sender, content=content).start()
        phone = {
            True: phone,
            False: None
        }[phone is not None and phone != ""]
        user = User.objects.create_user(email=email, password='123456')
        Profile.objects.create(user=user, name=name, phone=phone,
                               personal_email=personal_email, join_date=datetime.datetime.now())
