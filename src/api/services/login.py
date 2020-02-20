#!/usr/bin/env python

# author Huy
# date 8/14/2019

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from api.models import User
from api.services import BaseService, TokenUtil


class LoginService(BaseService):
    """
    LOGIN METHOD
    """

    @staticmethod
    def login(validate_data):
        try:
            user = User.objects.get(email=validate_data.get('email'))
            if not user.check_password(validate_data.get('password')):
                raise ValidationError("Invalid username or password")
            token = TokenUtil.encode(user)
            return {
                "success": True,
                "token": token,
                "user": user.id,
                "profile_id": user.profile.id,
                "email": user.email,
                "active": user.active,
                "admin": user.admin,
                "image": {
                    True: settings.MEDIA_IMAGE + '/media/' + str(user.profile.image),
                    False: None
                }[user.profile.image.name is not None and user.profile.image.name != ""]
            }
        except User.DoesNotExist:
            raise ValidationError("Invalid username or password")
        except Exception as e:
            raise e

    """
    CREATE USER AFTER VERIFIED SERVICE
    """

    @staticmethod
    def verify(data, password):
        user = User.objects.get(email=data.get('email'))
        user.password = make_password(password=password, salt=settings.SECRET_KEY)
        user.save()
