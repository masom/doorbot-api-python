from doorbot.factory import create_worker_app
from celery import Celery

app = create_worker_app()
celery = Celery('jobs', broker=app.config.get('CELERY_BROKER_URL'))
