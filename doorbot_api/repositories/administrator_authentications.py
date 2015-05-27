# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.administrator_authentication import AdministratorAuthentication


class AdministratorAuthentications(Repository):
    __model__ = AdministratorAuthentication
