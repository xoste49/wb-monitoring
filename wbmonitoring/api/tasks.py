# Create your tasks here

# from .models import Widget

from celery import shared_task
from celery.schedules import crontab


@shared_task
def parse_wb(s: str):
    pass