# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import reconstructor

from datetime import datetime
from ...core.model import DeclarativeBase, MutableDict, JsonType


class Integration(DeclarativeBase):
    __tablename__ = 'account_integrations'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)

    properties = Column(MutableDict.as_mutable(JsonType))

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True, default=datetime.utcnow)

    title = ""
    description = ""
    name = ""

    can_notify_users = False
    can_notify_group = False
    can_sync_users = False

    @reconstructor
    def reconstructor(self):
        self.initialize_properties()

    def initialize_properties(self):
        if not self.properties:
            self.properties = {}

    def fetch_users(self):
        raise NotImplementedError()

    def notify_user(self, notification):
        raise NotImplementedError()

    def notify_group(self, notification):
        raise NotImplementedError()

    def fields(self):
        return []

    def __getattr__(self, attr):

        if attr not in self.__properties__:
            raise AttributeError(
                'Attribute `{attr}` does not exists'.format(attr=attr)
            )

        value = self.properties.get(attr, None)
        if value:
            return value

        raise AttributeError(
            'Attribute `{attr}` does not exists'.format(attr=attr)
        )
