import os
from celery import Celery
from celery import signals

# Ustaw domyślne ustawienia Django dla programu 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amuman.settings')

app = Celery('amuman')

# Użyj ciągu znaków 'django.conf:settings', co oznacza, że konfiguracja Celery
# będzie automatycznie czytała z ustawień Twojego projektu Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Załaduj moduły zadań z wszystkich zarejestrowanych aplikacji Django.
app.autodiscover_tasks()

import pkgutil

@signals.worker_ready.connect
def at_start(sender, **kwargs):
    from node.tasks import run_node_at_startup
    run_node_at_startup.delay()