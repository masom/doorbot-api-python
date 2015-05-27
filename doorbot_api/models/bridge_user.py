# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from . import DeclarativeBase


class BridgeUser(DeclarativeBase):
    __tablename__ = 'bridge_users'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    person_id = Column(Integer)
    bridge_id = Column(Integer)
    bridge_user_id = Column(Integer)

    name = Column(String)
    email = Column(String)
    phone_number = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
