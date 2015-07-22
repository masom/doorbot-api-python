# -*- coding: utf-8 -*-

import os
from flask import Flask
from .container import container
from .db import db
from .schema_validator import jsonschema
from .sessions import ItsdangerousSessionInterface


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

        self.apps = {
            'admin': create_admin_app(config),
            'api': create_api_app(config),
            'public': create_public_app(config)
        }

        for name, app in self.apps.iteritems():
            app.debug = debug

        self.domain = domain

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

    from .views.api import (accounts, auth, people)

    app.register_blueprint(auth)
    app.register_blueprint(accounts)
    app.register_blueprint(people)

    return app
