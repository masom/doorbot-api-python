# -*- coding: utf-8 -*-

from flask import Flask

from .container import container
from .db import db


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_pyfile(config)

    app.url_map.strict_slashes = False

    db.init_app(app)
    container.init_app(app)

    from .views import (accounts, api, auth)

    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(accounts)

    return app
