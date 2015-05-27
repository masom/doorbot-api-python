# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String
from . import DeclarativeBase


class Event(DeclarativeBase):
    __tablename__ = 'events'

    account_id = Column(Integer)
    id = Column(Integer, primary_key=True)
    door_id = Column(Integer)
    device_id = Column(Integer)
    event_id = Column(Integer)
    person_id = Column(Integer)
    extra = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
