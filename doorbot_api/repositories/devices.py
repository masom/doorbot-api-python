# -*- coding: utf-8 -*-

from ..core.repository import Repository
from ..models.device import Device


class Devices(Repository):
    __model__ = Device
