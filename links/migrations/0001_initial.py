# Generated by Django 4.2.6 on 2023-10-26 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tracks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127)),
                ('description', models.TextField(blank=True, default='', max_length=1000)),
                ('url', models.URLField()),
                ('source_type', models.CharField(choices=[('YT', 'YouTube'), ('SP', 'Spotify'), ('UN', 'Unknown')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='links', to='tracks.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='LinkRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('fulfilled_at', models.DateTimeField(blank=True, null=True)),
                ('link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests', to='links.link')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='link_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Link Request',
                'verbose_name_plural': 'Link Requests',
            },
        ),
    ]