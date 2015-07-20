# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.notification import Notification


class Notifications(Repository):
    __model__ = Notification
