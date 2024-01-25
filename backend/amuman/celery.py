import os
from celery import Celery

# Ustaw domyślne ustawienia Django dla programu 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_queue.settings')

app = Celery('task_queue')

# Użyj ciągu znaków 'django.conf:settings', co oznacza, że konfiguracja Celery
# będzie automatycznie czytała z ustawień Twojego projektu Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Załaduj moduły zadań z wszystkich zarejestrowanych aplikacji Django.
app.autodiscover_tasks()
