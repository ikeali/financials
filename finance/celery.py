import os
from celery import Celery
from decouple import config

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance.settings')

app = Celery('finance')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.broker_url = config('CELERY_BROKER_URL')



