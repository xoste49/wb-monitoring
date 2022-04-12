import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wbmonitoring.settings')

app = Celery('wbmonitoring')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-hour2': {
        'task': 'api.tasks.parse_wb',
        'schedule': crontab(),
    },
}