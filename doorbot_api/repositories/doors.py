# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.door import Door


class Doors(Repository):
    __model__ = Door
