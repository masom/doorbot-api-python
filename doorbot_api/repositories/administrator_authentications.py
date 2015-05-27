# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.administrator_authentication import AdministratorAuthentication


class Accounts(Repository):
    __model__ = AdministratorAuthentication
