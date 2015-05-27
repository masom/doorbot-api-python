from flask import Flask

app = Flash(__name__)


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    from .routes import routes

    app.register_blueprint(routes)

    return app
