# -*- coding: utf-8 -*-

from ..db import db
from celery import Task


class DeliverNotificationJob(Task):
    ignore_result = True

    def run(self, notification_id):

        notification = db.session.query('Notification').filter_by(
            id=notification_id
        ).first()

        if not notification:
            return False
