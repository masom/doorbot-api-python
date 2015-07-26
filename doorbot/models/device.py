# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, ForeignKey, Index
)
from ..core.model import DeclarativeBase


class Device(DeclarativeBase):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)

    name = Column(String)
    device_id = Column(String)
    door_id = Column(Integer, ForeignKey("doors.id"), nullable=True)
    make = Column(String)
    description = Column(String)
    is_enabled = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    token = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)


Index('account_id_on_devices', Device.account_id)
Index('token_on_devices', Device.token, unique=True)
