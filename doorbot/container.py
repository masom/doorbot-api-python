# -*- coding: utf-8 -*-

from flask import _request_ctx_stack as stack

from .services import Services
from .repositories import Repositories
from .auth import Authorization
from .db import db


class Container(object):

    def init_app(self, app):
        app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def set_account_scope(self, id):
        ctx = stack.top
        if ctx is None:
            return None

        ctx.doorbot_account_id = id

    @property
    def authorization(self):
        ctx = stack.top

        if ctx is None:
            return None

        if not hasattr(ctx, 'doorbot_authorization'):
            ctx.doorbot_authorization = Authorization()

        return ctx.doorbot_authorization

    @property
    def account(self):
        ctx = stack.top

        if ctx is None:
            return None

        if not hasattr(ctx, 'doorbot_account'):
            return None

        if not hasattr(ctx, 'doorbot_account'):
            ctx.doorbot_account = self.repositories.accounts.first(
                id=ctx.doorbot_account_id
            )

        return ctx.doorbot_account

    @property
    def database_session(self):
        ctx = stack.top

        if ctx is None:
            return None

        if not hasattr(ctx, 'doorbot_database'):
            ctx.doorbot_database = db

        return ctx.doorbot_database.session

    @property
    def services(self):
        ctx = stack.top

        if ctx is None:
            return None

        if not hasattr(ctx, 'doorbot_services'):
            ctx.doorbot_services = Services(self.repositories)

        return ctx.doorbot_services

    @property
    def repositories(self):
        ctx = stack.top

        if ctx is None:
            return None

        if not hasattr(ctx, 'doorbot_repositories'):
            ctx.doorbot_repositories = Repositories(self.database_session)

        return ctx.doorbot_repositories

container = Container()
