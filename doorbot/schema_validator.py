# -*- coding: utf-8 -*-

"""
Originally Flask-JsonSchema

MIT License

Copyright (C) 2012 by Matthew Wright
"""

import os

from flask import current_app
from jsonschema import Draft4Validator

try:
    import simplejson as json
except ImportError:
    import json


class State(object):
    def __init__(self, schemas):
        self._schemas = schemas

    def get_schema(self, name):
        return self._schemas[name]


class JsonSchema(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self._state = self.init_app(app)

    def init_app(self, app):
        default_dir = os.path.join(app.root_path, 'jsonschema')
        schema_dir = app.config.get('JSONSCHEMA_DIR', default_dir)
        schemas = {}

        for fn in os.listdir(schema_dir):
            key = fn.split('.')[0]
            fn = os.path.join(schema_dir, fn)

            if os.path.isdir(fn) or not fn.endswith('.json'):
                continue

            with open(fn) as f:
                schemas[key] = json.load(f)
                Draft4Validator.check_schema(schemas[key])

        state = State(schemas)

        app.extensions['jsonschema'] = state

        return state

    def get(self, *path):
        return current_app.extensions['jsonschema'].get_schema(path)


jsonschema = JsonSchema()
