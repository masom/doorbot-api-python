# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, ForeignKey, Index
)
from sqlalchemy.orm import relationship

from ..core.model import DeclarativeBase


class Person(DeclarativeBase):
    __tablename__ = 'people'

    TYPE_MEMBER = 1
    TYPE_MANAGER = 2
    TYPE_OWNER = 3

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    account_type = Column(Integer)

    name = Column(String)
    title = Column(String)
    email = Column(String, nullable=False)
    phone_number = Column(String)
    is_visible = Column(Boolean, default=True, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    notifications_enabled = Column(Boolean, default=True, nullable=False)
    notifications_app_enabled = Column(Boolean, default=True, nullable=False)
    notifications_chat_enabled = Column(Boolean, default=False, nullable=False)
    notifications_email_enabled = Column(
        Boolean, default=False, nullable=False
    )
    notifications_sms_enabled = Column(Boolean, default=False, nullable=False)

    notifications = relationship("Notification", lazy="dynamic")
    authentications = relationship(
        "PersonAuthentication", lazy="dynamic", backref='person'
    )

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    def is_account_manager(self):
        return self.account_type == self.TYPE_OWNER or \
            self.account_type == self.TYPE_MANAGER

    def is_account_owner(self):
        return self.account_type == self.TYPE_OWNER

Index('account_id_on_people', Person.account_id)
Index(
    'unique_email_per_account_on_people', Person.account_id, Person.email,
    unique=True
)
