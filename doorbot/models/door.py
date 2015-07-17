# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from . import DeclarativeBase


class Door(DeclarativeBase):
    __tablename__ = 'doors'

    account_id = Column(Integer)
    id = Column(Integer, primary_key=True)
    name = Column(String)
