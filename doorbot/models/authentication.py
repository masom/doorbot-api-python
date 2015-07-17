# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from . import DeclarativeBase

PROVIDER_PASSWORD = 1
PROVIDER_API_TOKEN = 2


class Authentication(DeclarativeBase):
    __tablename__ = 'authentications'

    id = Column(Integer, primary_key=True)

    account_id = Column(Integer)
    person_id = Column(Integer)
    provider_id = Column(Integer)

    token = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)
