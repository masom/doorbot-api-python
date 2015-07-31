# -*- coding: utf-8 -*-
from flask import Flask
from .db import db
from celery import Celery

worker = Flask(__name__)
worker.config.from_pyfile('../config.py')
db.init_app(worker)

celery = Celery(__name__)
celery.conf.update(
    CELERY_IMPORTS=worker.config.get('CELERY_IMPORTS', ('doorbot.tasks',)),
    BROKER_URL=worker.config.get('CELERY_BROKER_URL'),
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
)
