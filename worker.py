from doorbot.factory import create_worker_app
from celery import Celery

app = create_worker_app('../config_debug.py')
celery = Celery('jobs', broker=app.config.get('CELERY_BROKER_URL'))
celery.conf.update(
    CELERY_ACCEPT_CONTENT=app.config.get('CELERY_ACCEPT_CONTENT')
)
