from flask import Flask
from .services import Services
from .repositories import Repositories


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.from_pyfile(config)

    from .views import (accounts, api, auth)

    repositories = Repositories()
    repositories.init_app(app)

    services = Services()
    services.init_app(app)

    app.doorbot_services = services
    app.doorbot_repositories = repositories
    app.doorbot_database = False

    app.register_blueprint(accounts)
    app.register_blueprint(api)
    app.register_blueprint(auth)

    return app
