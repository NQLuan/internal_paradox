__author__ = "hoangnguyen"
__date__ = "$Feb 17, 2020 23:57:48 PM$"

from api.errors import AuthErr
from api.models import User
from rest_framework import exceptions
from django.contrib.auth.hashers import make_password


def cmd_set_password():
    user_id = input("Enter user ID: ")
    pwd = input("Enter a new password: ")
    try:
        if len(pwd) < 6:
            error = AuthErr.PASSWORD_REQUIRED_CHARACTERS
            raise exceptions.ValidationError({'code': error.get('code'), 'message': error.get('message')})
        user = User.objects.get(id=user_id)
        user.password = make_password(pwd)
        user.save()
    except Exception as e:
        print(str(e))
