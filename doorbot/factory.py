# -*- coding: utf-8 -*-

import os
from flask import Flask
from .container import container
from .db import db
from .schema_validator import jsonschema
from .sessions import ItsdangerousSessionInterface
from .views.api.lib.json_serializer import ApiJsonEncoder


class SubdomainDispatcher(object):
    """Dispatch requests to a specific app based on the subdomain.
    """

    def __init__(self, domain, config=None, debug=False):
        '''
        :param domain: The domain the dispatcher is attached to.
        :type domain: string
        :param config:
        :param debug: Force debug
        :type debug: boolean
        '''

        self.config = config
        self.factories = {}
        self.apps = {}
        self.domain = domain
        self.debug = debug

    def add_app_factory(self, name, factory):
        self.factories[name] = factory

    def initialize(self):

        for name, factory in self.factories.items():
            self.apps[name] = factory(self.config)
            self.apps[name].debug = self.debug

    def get_application(self, environ):
        """Get the proper application for the given http environment
        :param environ: The environment dict
        """

        host = environ['HTTP_HOST'].split(':')[0]
        parts = host.split('.')

        if len(parts) != 3:
            return self.apps['public']

        if parts[0] == 'admin':
            return self.apps['admin']

        # Save the parsed subdomain to DOORBOT_ACCOUNT_HOST
        environ['DOORBOT_ACCOUNT_HOST'] = parts[0]
        return self.apps['api']

    def __call__(self, environ, start_response):
        app = self.get_application(environ)
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
    app.session_interface = ItsdangerousSessionInterface()

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


def create_api_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_pyfile(config)

    app.config['JSONSCHEMA_DIR'] = os.path.abspath('doorbot/views/api/schemas')

    app.url_map.strict_slashes = False

    jsonschema.init_app(app)
    db.init_app(app)
    container.init_app(app)

    from .views.api import (
        account, auth, devices, doors, integrations, notifications, people
    )

    app.json_encoder = ApiJsonEncoder
    app.register_blueprint(auth)
    app.register_blueprint(account)
    app.register_blueprint(devices)
    app.register_blueprint(doors)
    app.register_blueprint(integrations)
    app.register_blueprint(notifications)
    app.register_blueprint(people)

    return app
