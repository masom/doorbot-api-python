# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..core.model import DeclarativeBase


class Administrator(DeclarativeBase):
    __tablename__ = 'administrators'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    name = Column(String)

    is_deleted = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    authentications = relationship(
        "AdministratorAuthentication", lazy="dynamic"
    )
