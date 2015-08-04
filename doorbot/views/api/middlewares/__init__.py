# -*- coding: utf-8 -*-
import jsonschema
from flask import jsonify, request, current_app
from ....middlewares import (account_scope, auth_secured, _logger_context)
from structlog import get_logger

log = get_logger()


def validate(name):
    """Validate the request data with the given JSON schema name
    :param name: Name of the json schema
    :type name: string
    """

    def wrapped(*args, **kwargs):
        schema = current_app.extensions['jsonschema'].get_schema(name)

        try:
            jsonschema.validate(request.json, schema)
        except jsonschema.ValidationError as e:
            log.info("schema validation error", error=e)
            # TODO let the Flask error handler pickup this error.
            return {}, 422

    return wrapped


def handle_response(rv):
    """Handle rending the proper response
    :param rv: The return value from a view / middleware. Can be a tuple.
    """

    # Determine the best response type from the request.
    # Will be used to port response to JSONAPI
    best = request.accept_mimetypes.best_match([
        'application/json', 'application/vnd.json+api'
    ])

    if best == 'application/json':
        if isinstance(rv, tuple):
            rv, rc = rv
            return jsonify(rv), rc

        if isinstance(rv, dict):
            return jsonify(rv)
    else:
        return jsonify({}), 406


def s(*mw):
    '''s defines a list of route middlewares that will be applied in order.
    '''

    return m(account_scope, auth_secured, *mw)


def m(*mw):
    '''m defines a list of route middlewares that will be applied in order.
    '''

    def wrapped(*args, **kwargs):
        _logger_context()
        for item in mw:
            rv = item(*args, **kwargs)
            if rv:
                return handle_response(rv)

    return wrapped
