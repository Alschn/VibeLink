"""
Reference:

Adding periodic tasks via on_after_configure signal
- https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#entries
"""
import os

from celery import Celery, schedules

from links.queue.schedules import schedule_generate_link_requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs) -> None:
    # generate daily link requests at random time during the day
    sender.add_periodic_task(
        schedule=schedules.crontab(hour='0', minute='0'),
        sig=schedule_generate_link_requests.s(),
        name='daily-schedule-generate-link-requests',
    )
