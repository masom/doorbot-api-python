# -*- coding: utf-8 -*-


class Service(object):
    def __init__(self, services=None, database=None, account=None):
        self.services = services
        self.database = database
        self.account = account
