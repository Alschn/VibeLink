# Generated by Django 4.2.6 on 2023-10-26 14:07

from django.db import migrations, models
import django.db.models.deletion
import django_jsonform.models.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('meta', django_jsonform.models.fields.JSONField(
                    schema={
                        'type': 'dict',
                        'keys': {},
                        'additionalProperties': True,
                    },
                    blank=True, default=dict,
                    help_text='Additional information fetched from external source in JSON format')
                 ),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('meta', django_jsonform.models.fields.JSONField(
                    schema={
                        'type': 'dict',
                        'keys': {},
                        'additionalProperties': True,
                    },
                    blank=True, default=dict,
                    help_text='Additional information fetched from external source in JSON format')
                 ),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='tracks',
                    to='tracks.author')
                 ),
            ],
            options={
                'verbose_name': 'Track',
                'verbose_name_plural': 'Tracks',
            },
        ),
    ]
