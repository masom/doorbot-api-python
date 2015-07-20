# -*- coding: utf-8 -*-

from .accounts import Accounts
from .auth import Auth
from .host_generator import HostGenerator
from .notifications import Notifications


class Services(object):

    __services__ = dict(
        accounts=Accounts,
        auth=Auth,
        host_generator=HostGenerator,
        notifications=Notifications
    )

    def __init__(self, database, account=None):
        self._account = account
        self._database = database
        self._instances = dict()

    def __getattr__(self, attr):

        klass = self.__services__.get(attr, False)
        if klass is False:
            raise AttributeError(
                "Service `{attr}` is not registered".format(attr=attr)
            )

        service = self._instances.get(attr, None)
        if not service:
            service = klass(self, self._database, self._account)
            self._instances[attr] = service

        return service
