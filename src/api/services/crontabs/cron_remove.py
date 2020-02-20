from crontab import CronTab
from django.conf import settings


def remove():
    my_cron = CronTab(user=settings.UBUNTU_USER)
    for job in my_cron:
        my_cron.remove(job)
        my_cron.write()


remove()
