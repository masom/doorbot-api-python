# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy import event
from ..core.model import DeclarativeBase

PROVIDER_PASSWORD = 1
PROVIDER_API_TOKEN = 2


class PersonAuthentication(DeclarativeBase):
    __tablename__ = 'person_authentications'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    person_id = Column(Integer, ForeignKey("people.id"), nullable=False)
    provider_id = Column(Integer, nullable=False)

    token = Column(String, nullable=False)
    is_enabled = Column(Boolean, nullable=False, default=True)
    is_deleted = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)


def before_insert(mapper, connection, target):
    target.account_id = target.person.account_id

event.listen(PersonAuthentication, 'before_insert', before_insert)
