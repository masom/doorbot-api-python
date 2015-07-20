# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.service_user import ServiceUser


class ServiceUsers(Repository):
    __model__ = ServiceUser
