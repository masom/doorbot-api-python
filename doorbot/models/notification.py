# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from ..core.model import DeclarativeBase, JobStatuses
from .notification_delivery import NotificationDelivery
from structlog import get_logger
from ..db import db
logger = get_logger()


class Notification(DeclarativeBase):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    door_id = Column(Integer, ForeignKey('doors.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=True)
    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    deliveries = relationship(
        'NotificationDelivery', lazy='dynamic', backref='notification'
    )

    def send(self):
        integrations = self.account.integrations.filter_by(
            is_active=True
        ).all()

        for integration in integrations:

            delivery = NotificationDelivery()
            delivery.notification_id = self.id
            delivery.account_id = self.account_id
            delivery.integration_id = integration.id

            try:
                if self.person_id and \
                        integration.adapter.can_notify_users(self):

                    integration.adapter.notify_user(
                        self, delivery
                    )

                elif integration.can_notify_groups(self):
                    integration.adapter.notify_group(
                        self, delivery
                    )

            except Exception as e:
                delivery.response = str(e)
                delivery.status = JobStatuses.ERROR
                logger.error(
                    'Notification delivery error',
                    error=e,
                    account_id=self.account_id,
                    notification_id=self.id,
                    integration_id=integration.id
                )

            print(delivery.response)
            self.deliveries.append(delivery)

            db.session.commit()


Index('account_id_on_notifications', Notification.account_id)
