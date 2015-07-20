# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from ..core.model import DeclarativeBase


class ServiceUser(DeclarativeBase):
    __tablename__ = 'service_users'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    service = Column(String, nullable=False)
    service_user_id = Column(String, nullable=False)

    name = Column(String)
    email = Column(String)
    phone_number = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
