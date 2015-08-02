# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import (
    Column, DateTime, Integer, String, ForeignKey, Index
)
from ..core.model import DeclarativeBase, MutableDict, JsonType


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
    title = Column(String)
    extra = Column(MutableDict.as_mutable(JsonType))

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

Index('account_id_on_service_users', ServiceUser.account_id)
Index(
    'unique_service_user_per_account_on_service_users',
    ServiceUser.account_id, ServiceUser.service, ServiceUser.service_user_id,
    unique=True
)
