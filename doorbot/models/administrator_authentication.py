# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey

from ..core.model import DeclarativeBase


class AdministratorAuthentication(DeclarativeBase):
    __tablename__ = 'administrator_authentications'

    id = Column(Integer, primary_key=True)

    administrator_id = Column(
        Integer, ForeignKey("administrators.id"), nullable=False
    )
    provider_id = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    token = Column(String, nullable=False)
    last_used_at = Column(DateTime)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
