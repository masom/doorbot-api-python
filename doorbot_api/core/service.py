# -*- coding: utf-8 -*-


class Service(object):
    def __init__(self, services=None, repositories=None):
        self._repositories = repositories
        self._services = services
