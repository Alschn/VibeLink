import inspect
from datetime import timedelta, datetime
from typing import Any
from typing import Callable

from django.db import connection
from django.utils import timezone
from django_q.models import Schedule
from django_q.tasks import async_task


def get_function_module_path(func: Callable) -> str:
    """
    Utility function used to resolve a path argument to async_task/schedule function.

    It helps to avoid hard coding paths to functions, which might change in the future.

    Instead of:
        task='path.to.module.function'

    Do this:
        from path.to.module import function

        task=get_function_module_path(function)
    """

    return f"{inspect.getmodule(func).__name__}.{func.__name__}"


def create_async_task(func: Callable, *args: Any, **kwargs: Any):
    """
    Wrapper around `django_q.tasks.async_task` function
    that automatically resolves a path to the given callable.
    """

    return async_task(
        get_function_module_path(func),
        *args,
        **kwargs
    )


def assure_scheduled(
    schedule_func: Callable[..., Schedule],
    name: str,
    recreate: bool = False,
    *args,
    **kwargs
) -> Schedule | None:
    """
    Checks if a schedule with given name exists and if not, creates it.
    If it exists, then it is deleted and recreated to ensure its details are up-to-date.
    """
    tables = connection.introspection.table_names()

    if Schedule._meta.db_table not in tables:
        print(
            f'Schedule table not in database, "{schedule_func.__name__}" not scheduled, '
            f'please run migrations and restart the app'
        )
        return

    queryset = Schedule.objects.filter(name=name)

    if queryset.exists():
        if recreate:
            print(f"Schedule with name `{name}` already exists. Recreating...")
            queryset.delete()
            return schedule_func(*args, **kwargs, name=name)

        print(f"Schedule with name `{name}` already exists. Skipping...")
        return queryset.first()

    print(f"Creating schedule with name `{name}`...")
    return schedule_func(*args, **kwargs, name=name)


def get_daily_schedule_next_run_time(
    *, hour: int, minute: int,
    second: int = 0, microsecond: int = 0
) -> datetime:
    now = timezone.now()
    return now.replace(
        hour=hour, minute=minute,
        second=second, microsecond=microsecond
    ) + timedelta(days=1)
