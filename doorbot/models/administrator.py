# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String

from . import DeclarativeBase


class Administrator(DeclarativeBase):
    __tablename__ = 'administrators'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
