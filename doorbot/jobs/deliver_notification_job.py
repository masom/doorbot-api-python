# -*- coding: utf-8 -*-

from .background_job import BackgroundJob
from ..db import db


class DeliverNotificationJob(BackgroundJob):
    def run(self, notification_id):

        notification = db.session.query('Notification').filter_by(
            id=notification_id
        ).first()

        if not notification:
            pass
