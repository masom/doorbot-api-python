# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..core.model import DeclarativeBase


class Person(DeclarativeBase):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    account_type = Column(Integer)

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

    notifications = relationship("Notification", lazy="dynamic")
    authentications = relationship("PersonAuthentication", lazy="dynamic")

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    def is_account_manager(self):
        return False

    def is_account_owner(self):
        return False
