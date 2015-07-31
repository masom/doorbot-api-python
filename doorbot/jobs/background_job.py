# -*- coding: utf-8 -*-

from ..worker import celery, worker


class BackgroundJob(celery.Task):
    ignore_result = True
    abstract = True
    serializer = 'json'

    def __call__(self, *args, **kwargs):
        # Setup the Flask app context
        with worker.app_context():
            super(BackgroundJob, self).__call__(*args, **kwargs)
