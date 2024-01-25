"""
Django settings for amuman project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from .settings import *
from celery.schedules import crontab

INSTALLED_APPS += [
    "master",
]

URL_MODE_PREFIX = 'master'  # Prefiks URL dla trybu klienta

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "masterdb.sqlite3", 
    }
}


CELERY_BEAT_SCHEDULE = {
    'check-node-status-every-minute': {
        'task': 'scheduler.tasks.check_node_status',
        'schedule': crontab(minute='*/1'),
    },
}