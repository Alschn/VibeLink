import random

from celery import shared_task
from django.utils import timezone

from core.shared.tasks import get_function_module_path
from links.queue.tasks import generate_link_requests


@shared_task
def schedule_generate_link_requests() -> str:
    from django_celery_beat.models import PeriodicTask, ClockedSchedule

    now = timezone.now()
    end_of_today = now.replace(hour=23, minute=59, second=59)

    # get random time during the day
    random_time = now + timezone.timedelta(
        seconds=random.randint(0, (end_of_today - now).total_seconds())
    )

    task_name = 'generate-link-requests-' + random_time.strftime('%Y-%m-%d-%H-%M-%S')

    # create a new schedule required by periodic task
    clocked, _ = ClockedSchedule.objects.get_or_create(clocked_time=random_time)

    # schedule one-off task at random time
    PeriodicTask.objects.create(
        name=task_name,
        task=get_function_module_path(generate_link_requests),
        one_off=True,
        clocked=clocked,
        start_time=random_time,
    )

    return task_name
