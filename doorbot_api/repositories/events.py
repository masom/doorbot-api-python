# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.event import Event


class Events(Repository):
    __model__ = Event
