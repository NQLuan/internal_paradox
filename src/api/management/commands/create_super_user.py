__author__ = "hoangnguyen"
__date__ = "$Feb 17, 2020 23:57:48 PM$"

from django.contrib.auth.hashers import make_password

from . import CustomBaseCommand

from api.models import Profile, User

from django.db import transaction


class Command(CustomBaseCommand):
    help = "Create Super User"
    validate_admin = True

    def handle_admin_access(self, *args, **options):
        admin_email = input("Enter the admin email: ")
        admin_pass = input("Enter the admin password: ")
        admin_user = User.objects.filter(is_superuser=True).exists()
        if not admin_user:
            try:
                with transaction.atomic():
                    admin_user = User()
                    admin_user.email = admin_email
                    admin_user.password = make_password(admin_pass)
                    admin_user.staff = True
                    admin_user.admin = True
                    admin_user.active = True
                    admin_user.is_superuser = True
                    admin_user.save()
                    Profile.objects.create(user=admin_user, name="Admin")

            except Exception as e:
                print(e)
