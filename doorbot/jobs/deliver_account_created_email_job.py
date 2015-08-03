# -*- coding: utf-8 -*-

from ..db import db
from .background_job import BackgroundJob
from ..models import Account
from structlog import get_logger


class DeliverAccountCreatedJob(BackgroundJob):
    ignore_result = True

    def run(self, account_id):

        account = db.session.query(Account).filter_by(id=account_id).first()

        if not account:
            logger.warning(
                'DeliverAccountCreatedJob account not found',
                account_id=account_id
            )
            return False

        
