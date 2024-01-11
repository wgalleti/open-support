from __future__ import absolute_import
import os
from celery import Celery

from suporte import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suporte.settings')
app = Celery('suporte')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
