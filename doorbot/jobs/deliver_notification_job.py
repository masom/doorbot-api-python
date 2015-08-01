# -*- coding: utf-8 -*-

from ..db import db
from .background_job import BackgroundJob
from ..models import Notification
from structlog import get_logger
logger = get_logger()


class DeliverNotificationJob(BackgroundJob):
    ignore_result = True

    def run(self, notification_id):

        notification = db.session.query(Notification).filter_by(
            id=notification_id
        ).first()

        if not notification:
            logger.warning(
                'DeliverNotificationJob notification not found',
                notification_id=notification_id
            )
            return False

        try:
            notification.send()
        except Exception as e:
            logger.error(
                'DeliverNotificationJob failed',
                error=e,
                notification_id=notification_id
            )
            raise e
