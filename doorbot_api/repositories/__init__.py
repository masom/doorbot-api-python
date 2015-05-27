# -*- coding: utf-8 -*-

from flask import _app_ctx_stack as stack

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

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, app):
        pass

    def __getattr__(self, attr):

        if hasattr(self, attr):
            return getattr(self, attr)

        ctx = stack.top

        if ctx is None:
            raise AttributeError()

        klass = self.__repositories__.get(attr, False)
        if klass is False:
            raise AttributeError('Attribute %s is not defined' % attr)

        if not hasattr(ctx, 'doorbot_repositories'):
            ctx.doorbot_repositories = dict()

        repo = ctx.doorbot_repositories.get(attr, None)
        if not repo:
            repo = klass(ctx.doorbot_database)
            ctx.doorbot_repositories[attr] = repo

        repo.set_account_scope(ctx.account_id)
        return repo

    def database_session(self):
        return self._database.session

    def set_account_scope(self, account_id):
        self.account_id = account_id

        [repo.set_account_scope(account_id)
         for repo in self._instances.iteritems()]
