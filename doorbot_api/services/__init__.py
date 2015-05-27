# -*- coding: utf-8 -*-


from .accounts import Accounts
from .host_generator import HostGenerator

class Services(object):

    __services__ = dict(
        accounts=Accounts,
        host_generator=HostGenerator,
    )

    def __init__(self, repositories):
        self._repositories = repositories
        self._instances = dict()
    
    def __getattr__(self, attr):

        klass = self.__services__.get(attr, False)
        if repo is False:
            raise AttributeError()

        repo = self._instances.get(attr, None)
        if not repo:
            repo = klass(self, self._repositories)
            self._instances[attr] = repo

        return repo
