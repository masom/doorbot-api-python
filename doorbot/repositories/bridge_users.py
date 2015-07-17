# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.bridge_user import BridgeUser


class BridgeUsers(Repository):
    __model__ = BridgeUser
