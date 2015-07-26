# -*- coding: utf-8 -*-

from sqlalchemy import (
    Boolean, Column, Integer, String, ForeignKey, DateTime, Index
)
from datetime import datetime
from ..core.model import DeclarativeBase


class Door(DeclarativeBase):
    __tablename__ = 'doors'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    name = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_deleted = Column(Boolean, nullable=False, default=False)


Index('account_id_on_doors', Door.account_id)
