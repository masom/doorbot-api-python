# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.administrator import Administrator


class Administrators(Repository):
    __model__ = Administrator
