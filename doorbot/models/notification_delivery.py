# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import (
    Column, DateTime, Integer, ForeignKey, Text, Enum
)
from ..core.model import DeclarativeBase, JobStatuses


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

    status = Column(
        Enum(*JobStatuses.to_list()), nullable=False,
        default=JobStatuses.PENDING
    )

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
