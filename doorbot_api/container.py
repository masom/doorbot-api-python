# -*- coding: utf-8 -*-

from flask import _app_ctx_stack as stack

from .services import Services
from .repositories import Repositories
from .db import db


class Container(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        pass

    @property
    def database_session(self):
        return db.session

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
