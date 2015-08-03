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

        sync.status = JobStatuses.RUNNING
        db.session.commit()

        try:
            sync.synchronize()
            sync.status = JobStatuses.SUCCESS
        except Exception as e:
            import traceback

            logger.error(
                'synchronization error',
                error=e, people_synchronization_id=sync.id,
                account_id=sync.account_id,
                trace=traceback.format_exc()
            )
            db.session.rollback()

            sync.status = JobStatuses.ERROR

            db.session.commit()
            return False

        db.session.commit()
