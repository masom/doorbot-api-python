# -*- coding: utf-8 -*-

from .background_job import BackgroundJob
from ..db import db
from structlog import get_logger
from celery import shared_task
logger = get_logger()


@shared_task()
class SynchronizePeopleJob(BackgroundJob):

    def run(self, people_synchronization_id):

        sync = db.session.query('PeopleSynchronization').filter_by(
            id=people_synchronization_id
        ).first()

        if not sync:
            return False

        try:
            sync.synchronize()
        except Exception as e:
            logger.error(
                'synchronization error',
                error=e, people_synchronization_id=sync.id,
                account_id=sync.account_id
            )
            return False
