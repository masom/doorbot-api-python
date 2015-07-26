# -*- coding: utf-8 -*-
from celery import Task


class BackgroundJob(Task):
    # Ignore results by default
    ignore_result = True
    timeout = 10

    def run(self, *args, **kwargs):
        raise NotImplementedError('perform must be implemented')
