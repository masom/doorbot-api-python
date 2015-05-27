# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from . import DeclarativeBase


class Person(DeclarativeBase):
    __tablename__ = 'people'

    account_id = Column(Integer)
    account_type = Column(Integer)
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    email = Column(String)
    phone_number = Column(String)
    is_visible = Column(Boolean)
    is_available = Column(Boolean)

    notifications_enabled = Column(Boolean)
    notifications_app_enabled = Column(Boolean)
    notifications_email_enabled = Column(Boolean)
    notifications_sms_enabled = Column(Boolean)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    def is_account_manager(self):
        return False

    def is_account_owner(self):
        return False
