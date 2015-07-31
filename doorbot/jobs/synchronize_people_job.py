# -*- coding: utf-8 -*-

from ..db import db
from structlog import get_logger
from .background_job import BackgroundJob
logger = get_logger()


class SynchronizePeopleJob(BackgroundJob):

    ignore_result = True
    timeout = 10

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
