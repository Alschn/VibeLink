from typing import Any

from django.contrib.sites.models import Site
from django.core.management import BaseCommand, CommandParser


class Command(BaseCommand):
    """
    Creates a new Site object with the given domain and name.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            'domain',
            type=str,
            help='Unique domain for the site. Should include protocol and port.'
        )
        parser.add_argument(
            'name',
            type=str,
            help='Display name for the site.'
        )

    def handle(self, *args: Any, **options: Any) -> None:
        unique_domain = options['domain']
        display_name = options['name']

        if not unique_domain.startswith('http'):
            self.stdout.write(
                self.style.WARNING(
                    f'Invalid domain {unique_domain}. Must start with http or https.'
                )
            )
            return

        if Site.objects.filter(name=display_name).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Site with display name {display_name} already exists.'
                )
            )
            return

        if Site.objects.filter(domain=unique_domain).exists():
            self.stdout.write(
                self.style.WARNING(
                    f'Site with domain {unique_domain} already exists.'
                )
            )
            return

        site = Site.objects.create(
            domain=unique_domain,
            name=display_name
        )
        self.stdout.write(
            self.style.SUCCESS(f'Site {site.name} {site.domain} created.')
        )
