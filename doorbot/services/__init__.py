# -*- coding: utf-8 -*-

from .accounts import Accounts
from .auth import Auth
from .host_generator import HostGenerator


class Services(object):

    __services__ = dict(
        accounts=Accounts,
        auth=Auth,
        host_generator=HostGenerator,
    )

    def __init__(self, repositories):
        self._repositories = repositories
        self._instances = dict()

    def __getattr__(self, attr):

        klass = self.__services__.get(attr, False)
        if klass is False:
            raise AttributeError()

        repo = self._instances.get(attr, None)
        if not repo:
            repo = klass(self, self._repositories)
            self._instances[attr] = repo

        return repo
