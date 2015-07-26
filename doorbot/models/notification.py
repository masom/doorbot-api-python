# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..core.model import DeclarativeBase
from .notification_delivery import NotificationDelivery
from ..jobs import DeliverNotificationJob


class Notification(DeclarativeBase):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    door_id = Column(Integer, ForeignKey('doors.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=False)
    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    deliveries = relationship(
        'NotificationDelivery', lazy='dynamic', backref='notification'
    )

    def schedule(self):
        DeliverNotificationJob().delay(self.id)

    def send(self):
        integrations = self.account.integrations.filter_by(
            is_enabled=True, is_deleted=False
        ).all()

        for integration in integrations:
            # TODO allow sending notifications to a group vs a person
            if self.person_id:
                if integration.can_notify_users:
                    delivery = NotificationDelivery()
                    delivery.notification_id = self.id
                    delivery.account_id = self.account_id
                    delivery.integration_id = integration.id

                    try:
                        delivery.response = integration.adapter.notify_user()
                        delivery.successful = True
                    except Exception as e:
                        delivery.response = e
                        delivery.successful = False

                    self.deliveries.append(delivery)

            elif integration.can_notify_group:
                pass
