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

INSTALLED_APPS += [
    "node",
    # 'node_app.apps.NodeAppConfig',
]

URL_MODE_PREFIX = 'node'  # Prefiks URL dla trybu klienta

DATABASES.update({
    'default': {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "nodedb.sqlite3",
    }
})

MIDDLEWARE += [
    # ... inne middleware ...
    'node.middleware.gpu_monitor_middleware.GPUMonitorMiddleware',
    'node.middleware.node_register_middleware.NodeStartupMiddleware',
    # 'node.middleware.websocket_check_middleware.WebSocketMiddleware',
]
PORT=8001

