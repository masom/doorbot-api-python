# -*- coding: utf-8 -*-

from flask import Flask

from .container import container
from .db import db


class SubdomainDispatcher(object):

    def __init__(self, domain, config=None, debug=False):
        self.apps = {
            'admin': create_admin_app(config),
            'scoped': create_scoped_app(config),
            'public': create_public_app(config)
        }

        for name, app in self.apps.iteritems():
            app.debug = debug

        self.domain = domain

    def get_application(self, host):
        host = host.split(':')[0]
        parts = host.split('.')

        if len(parts) != 3:
            return self.apps['public']

        if parts[0] == 'admin':
            return self.apps['admin']

        return self.apps['scoped']

    def __call__(self, environ, start_response):
        app = self.get_application(environ['HTTP_HOST'])
        return app(environ, start_response)


def create_admin_app(config=None):
    app = Flask(__name__)
    if config:
        app.config.from_pyfile(config)

    app.url_map.strict_slashes = False

    db.init_app(app)
    container.init_app(app)

    from .views.admin import (accounts)

    app.register_blueprint(accounts)

    return app


def create_public_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_pyfile(config)

    app.url_map.strict_slashes = False

    db.init_app(app)
    container.init_app(app)

    from .views.public import (public)

    app.register_blueprint(public)

    return app


def create_scoped_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_pyfile(config)

    app.url_map.strict_slashes = False

    db.init_app(app)
    container.init_app(app)

    from .views.scoped import (accounts, auth)

    app.register_blueprint(auth)
    app.register_blueprint(accounts)

    return app
