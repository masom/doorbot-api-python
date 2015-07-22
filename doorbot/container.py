# -*- coding: utf-8 -*-

from flask import _request_ctx_stack as stack

from .services import Services
from .auth import Authorization
from .db import db


class Container(object):

    def init_app(self, app):
        app.teardown_request(self.teardown)

    def teardown(self, exception):
        pass

    def set_account(self, account):
        ctx = stack.top
        if ctx is None:
            raise RuntimeError('Missing app context')

        ctx.doorbot_account = account

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

        return ctx.doorbot_account

    @property
    def database(self):
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
            ctx.doorbot_services = Services(self.database, self.account)

        return ctx.doorbot_services

container = Container()
