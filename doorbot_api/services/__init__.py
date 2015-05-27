# -*- coding: utf-8 -*-

from flask import _app_ctx_stack as stack

from .accounts import Accounts
from .host_generator import HostGenerator
from .. import repositories


class Services(object):

    __services__ = dict(
        accounts=Accounts,
        host_generator=HostGenerator,
    )

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        pass

    def __getattr__(self, attr):

        ctx = stack.top
        if ctx is None:
            raise AttributeError()

        klass = self.__services__.get(attr, False)
        if klass is False:
            raise AttributeError()

        if not hasattr(ctx, 'doorbot_services'):
            ctx.doorbot_services = dict()

        repo = ctx.doorbot_services.get(attr, None)
        if not repo:
            repo = klass(self, repositories)
            ctx.doorbot_services[attr] = repo

        return repo
