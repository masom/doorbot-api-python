# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column, Integer, Boolean, DateTime, String, event, Index
)
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import reconstructor

from datetime import datetime
from ..core.model import DeclarativeBase, MutableDict, JsonType
from .integrations import available_integrations


class Integration(DeclarativeBase):
    __tablename__ = 'integrations'

    id = Column(Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    properties = Column(MutableDict.as_mutable(JsonType))

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name
        self.reconstructor()

        if not self.adapter:
            raise ValueError(
                'Integration {name} is not available'.format(name=name)
            )

    @reconstructor
    def reconstructor(self):
        self.adapter = None
        self.initialize_properties()

        for integration in available_integrations:
            if integration.name == self.name:
                self.adapter = integration(self)
                break

    def initialize_properties(self):
        if not self.properties:
            self.properties = {}


def before_insert(mapper, connection, target):
    target.name = target.adapter.name

event.listen(Integration, 'before_insert', before_insert)

Index('account_id_on_integrations', Integration.account_id)
