import random

from django.utils import timezone
from django_q.models import Schedule
from django_q.tasks import schedule

from core.shared.tasks import (
    get_function_module_path,
    get_daily_schedule_next_run_time
)
from links.queue.tasks import generate_link_requests


def schedule_daily_generate_link_requests(*args, **kwargs) -> Schedule:
    return schedule(
        get_function_module_path(schedule_generate_link_requests),
        *args,
        schedule_type=Schedule.DAILY,
        repeats=-1,
        next_run=get_daily_schedule_next_run_time(hour=0, minute=0),
        **kwargs,
    )


def schedule_generate_link_requests() -> Schedule:
    now = timezone.now()
    end_of_today = now.replace(hour=23, minute=59, second=59)

    # get random time during the day
    random_time = now + timezone.timedelta(
        seconds=random.randint(0, (end_of_today - now).total_seconds())
    )

    task_name = 'generate-link-requests-' + random_time.strftime('%Y-%m-%d-%H-%M-%S')

    return schedule(
        get_function_module_path(generate_link_requests),
        name=task_name,
        schedule_type=Schedule.ONCE,
        next_run=random_time
    )
