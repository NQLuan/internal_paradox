from crontab import CronTab
from django.conf import settings


def add():
    my_cron = CronTab(user=settings.UBUNTU_USER)
    for job in my_cron:
        if job.comment == "leave_notification":
            my_cron.remove(job)
            my_cron.write()

    job = my_cron.new(
        command=f"cd /home/thanhhuy3411/company-api/src/api/services/crontabs/ && "
                f"python -c 'from leave_notification import leave_notification; leave_notification()'",
        comment="leave_notification")
    job.day.every(1)
    job.hour.also.on(9)
    job.minute.also.on(0)
    my_cron.write()


add()
