# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, Integer, ForeignKey, Text
from ..core.model import DeclarativeBase


class NotificationDelivery(DeclarativeBase):
    __tablename__ = 'notification_deliveries'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)

    notification_id = Column(
        Integer, ForeignKey('notifications.id'), nullable=False
    )

    integration_id = Column(
        Integer, ForeignKey('integrations.id'), nullable=False
    )

    response = Column(Text)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    successful = Column(Boolean, nullable=False, default=False)
