# -*- coding: utf-8 -*-

from ..db import db
from structlog import get_logger
from .background_job import BackgroundJob
from ..models import PeopleSynchronization
from ..core.model import JobStatuses
logger = get_logger()


class SynchronizePeopleJob(BackgroundJob):

    ignore_result = True
    timeout = 10

    def run(self, people_synchronization_id):

        sync = db.session.query(PeopleSynchronization).filter_by(
            id=people_synchronization_id
        ).first()

        if not sync:
            logger.warning(
                'SynchronizePeopleJob instance not found',
                people_synchronization_id=people_synchronization_id,
            )
            return False

        try:
            sync.synchronize()
        except Exception as e:
            logger.error(
                'synchronization error',
                error=e, people_synchronization_id=sync.id,
                account_id=sync.account_id
            )
            sync.status = JobStatuses.ERROR
            db.session.commit()
            return False
