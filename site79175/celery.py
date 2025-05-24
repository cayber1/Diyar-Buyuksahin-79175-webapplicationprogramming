import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site79175.settings')

app = Celery('site79175')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
