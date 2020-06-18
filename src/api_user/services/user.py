import datetime

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string

from api_base.services import BaseService, TokenUtil, SendMail
from api_user.models import User, Profile


class UserService(BaseService):

    @classmethod
    def get_user_by_id(cls, pk):
        user = User.objects.filter(pk=pk).first()
        return user

    @classmethod
    def get_user_by_email(cls, email):
        user = User.objects.filter(email=email).first()
        return user

    @classmethod
    def activate_user(cls, user):
        user.active = True
        user.save()

    @classmethod
    def deactivate_user(cls, user):
        user.active = False
        user.save()
        user.profile.teams = None
        user.profile.save()

    @classmethod
    def update_password(cls, data, user):
        try:
            current_password = data.get('current_password', None)
            hash_password = make_password(password=current_password, salt=settings.SECRET_KEY)
            if current_password is not None and current_password != "" and user.password != hash_password:
                raise Exception("Error: Password does not match")
            user.set_password(data.get('new_password'))
            return user
        except Exception:
            return None

    @classmethod
    def invite(cls, email, name):
        cls.send_mail(email=email, name=name, send_email=True)
        return {
            "success": True,
            "user": {
                'name': name,
                'email': email
            }
        }

    @classmethod
    def send_mail(cls, email=None, name=None, phone=None, personal_email=None, send_email=False):
        if send_email:
            token = TokenUtil.verification_encode(name, email, phone, personal_email)
            # TODO: Look at the link again
            link = f'http://{settings.API_HOST}/verify?token={token}'
            content = render_to_string('../templates/invitation_email.html',
                                       {'name': name, 'email': email, 'link': link, 'token': token})
            SendMail.start([email, personal_email], 'Welcome to Company Management', content)

        if phone == "":
            phone = None
        user = User.objects.create_user(email=email, password='123456')
        Profile.objects.create(user=user, name=name, phone=phone,
                               personal_email=personal_email, join_date=datetime.datetime.now())
