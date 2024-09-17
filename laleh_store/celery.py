import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'laleh_store.settings.dev')

celery = Celery('laleh_store')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks