from django.apps import AppConfig


class LinksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'links'

    def ready(self) -> None:
        from core.shared.tasks import assure_scheduled
        from links.queue.schedules import schedule_daily_generate_link_requests

        assure_scheduled(
            schedule_daily_generate_link_requests,
            name='schedule_daily_generate_link_requests'
        )
