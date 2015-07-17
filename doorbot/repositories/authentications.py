# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.authentication import Authentication


class Authentications(Repository):
    __model__ = Authentication
