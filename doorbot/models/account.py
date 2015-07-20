# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..core.model import DeclarativeBase
from .integrations import available_integrations

ACCOUNT_TYPE_MEMBER = 1
ACCOUNT_TYPE_MANAGER = 2
ACCOUNT_TYPE_OWNER = 3


class Account(DeclarativeBase):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    is_enabled = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    host = Column(String, nullable=False)

    contact_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    contact_email_confirmed = Column(Boolean, default=False)
    contact_phone_number = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    integrations = relationship("Integration", lazy="dynamic")
    devices = relationship("Device", lazy="dynamic")
    doors = relationship("Door", lazy="dynamic")
    events = relationship("Event", lazy="dynamic")
    people = relationship("Person", lazy="dynamic")
    service_users = relationship("ServiceUser", lazy="dynamic")

    def create_missing_integration(self, name):
        try:
            klass = next(i for i in available_integrations if i.name == name)
        except StopIteration:
            return None

        integration = klass()
        self.integrations.append(integration)

        return integration
