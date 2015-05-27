# -*- coding: utf-8 -*-

from .accounts import Accounts
from .administrator_authentications import AdministratorAuthentications
from .administrators import Administrators
from .authentications import Authentications
from .bridge_users import BridgeUsers
from .devices import Devices
from .doors import Doors
from .events import Events
from .people import People


class Repositories(object):

    __repositories__ = dict(
        accounts=Accounts,
        administrators=Administrators,
        administrator_authentication=AdministratorAuthentications,
        authentications=Authentications,
        bridgeUsers=BridgeUsers,
        devices=Devices,
        doors=Doors,
        events=Events,
        people=People
    )

    def __init__(self, database):
        self._database = database
        self._instances = dict()
        self.account_id = 0

    def __getattr__(self, attr):

        klass = self.__repositories__.get(attr, False)
        if klass is False:
            raise AttributeError()

        repo = self._instances.get(attr, None)
        if not repo:
            repo = klass(self._database)
            self._instances[attr] = repo

        repo.set_account_scope(self.account_id)
        return repo

    def database_session(self):
        return self._database.session

    def set_account_scope(self, account_id):
        self.account_id = account_id

        [repo.set_account_scope(account_id)
         for repo in self._instances.iteritems()]
