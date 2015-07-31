# -*- coding: utf-8 -*-

from ..db import db
from .background_job import BackgroundJob
from ..models import Notification


class DeliverNotificationJob(BackgroundJob):
    ignore_result = True

    def run(self, notification_id):

        print(notification_id)
        notification = db.session.query(Notification).filter_by(
            id=notification_id
        ).first()

        if not notification:
            print("No notification")
            return False

        try:
            notification.send()
        except Exception as e:
            raise e
