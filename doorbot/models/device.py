# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from . import DeclarativeBase


class Device(DeclarativeBase):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)

    name = Column(String)
    device_id = Column(String)
    door_id = Column(Integer)
    make = Column(String)
    description = Column(String)
    is_enabled = Column(Boolean, default=False)

    token = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
