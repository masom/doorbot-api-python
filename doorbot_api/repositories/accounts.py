# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.account import Account


class Accounts(Repository):
    __model__ = Account
