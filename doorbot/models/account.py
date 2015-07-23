# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..core.model import DeclarativeBase
from .integrations import available_integrations


class Account(DeclarativeBase):
    __tablename__ = 'accounts'


    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    is_enabled = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    host = Column(String, nullable=False)

    contact_name = Column(String, nullable=False)
    contact_email = Column(String, nullable=False)
    contact_email_confirmed = Column(Boolean, default=False, nullable=False)
    contact_phone_number = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    devices = relationship("Device", lazy="dynamic")
    doors = relationship("Door", lazy="dynamic")
    integrations = relationship("Integration", lazy="dynamic")
    notifications = relationship("Notification", lazy="dynamic")
    people = relationship("Person", lazy="dynamic", backref='account')
    service_users = relationship("ServiceUser", lazy="dynamic")

    def create_missing_integration(self, name):
        try:
            klass = next(i for i in available_integrations if i.name == name)
        except StopIteration:
            return None

        integration = klass()
        self.integrations.append(integration)

        return integration
