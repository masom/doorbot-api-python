# -*- coding: utf-8 -*-

from flask import Flask

from .container import container
from .db import db


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_pyfile(config)

    from .views import (accounts, api, auth)

    container.init_app(app)
    db.init_app(app)

    app.register_blueprint(accounts)
    app.register_blueprint(api)
    app.register_blueprint(auth)

    return app
