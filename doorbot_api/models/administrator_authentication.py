# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from . import DeclarativeBase


class AdministratorAuthentication(DeclarativeBase):
    __tablename__ = 'administrator_authentications'

    id = Column(Integer, primary_key=True)

    administrator_id = Column(Integer)
    provider_id = Column(Integer)

    token = Column(String)
    last_used_at = Column(DateTime)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
