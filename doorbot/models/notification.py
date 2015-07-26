# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..core.model import DeclarativeBase


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
