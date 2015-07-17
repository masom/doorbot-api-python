# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String

from . import DeclarativeBase

ACCOUNT_TYPE_MEMBER = 1
ACCOUNT_TYPE_MANAGER = 2
ACCOUNT_TYPE_OWNER = 3


class Account(DeclarativeBase):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    is_enabled = Column(Boolean, default=False)
    host = Column(String, nullable=False)

    contact_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    contact_email_confirmed = Column(Boolean, default=False)
    contact_phone_number = Column(String)

    notifications_enabled = Column(Boolean, default=False)
    notifications_email_enabled = Column(Boolean, default=False)
    notifications_email_message_template = Column(String)

    notifications_sms_enabled = Column(Boolean, default=False)
    notifications_sms_message_template = Column(String, nullable=True)
    notifications_sms_source_phone_number = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)
