from crontab import CronTab
from django.conf import settings


def add():
    my_cron = CronTab(user=settings.UBUNTU_USER)
    for job in my_cron:
        if job.comment == 'lunch_creation':
            my_cron.remove(job)
            my_cron.write()
    job = my_cron.new(
        command=f"cd /home/thanhhuy3411/company-api/src/api/services/crontabs/ && "
                f"python -c 'from lunch_creation import lunch_creation; lunch_creation()'",
        comment='lunch_creation')
    job.month.every(1)
    job.day.also.on(1)
    job.hour.also.on(6)
    job.minute.also.on(30)
    my_cron.write()


add()
