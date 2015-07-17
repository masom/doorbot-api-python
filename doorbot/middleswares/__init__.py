# -*- coding: utf-8 -*-

from flask import jsonify, request, current_app
import jsonschema
from ..container import container
from .. import auth
import logging

logger = logging.getLogger(__name__)

def _log_unauthorized_access(**context):
    context['module'] = __name__
    logger.info("{method} unauthorized access", context);

def m(*args):
    '''m defines a list of route middlewares that will be applied in order.
    '''

    def wrapped(*args, **kwargs):
        for item in args:
            ret = item(*args, **kwargs)
            if ret:
                return ret

    return wrapped


def auth_admin():
    if container.authorization.is_administrator():
        return

    return jsonify(dict()), 403


def auth_gatekeeper():
    pass


def auth_owner():
    authorization = container.authorization

    if authorization.is_person() and authorization.person.is_account_owner():
        return

    return jsonify(dict()), 403


def auth_secured():
    (mode, token) = auth.parse_token_authorization(
        request.headers.get('Authorization', None)
    )

    if not mode or not token:
        return jsonify(dict()), 401

    authorization = container.authorization
    if mode == auth.AUTHORIZATION_DEVICE:
        device = container.services.auth.device_with_token(token)
        if not device:
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )

            return jsonify(dict()), 401

        authorization.update_to_device(device)

    elif mode == auth.AUTHORIZATION_PERSON:
        person = container.services.auth.person_with_token(token)
        if not person:
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )

            return jsonify(dict()), 401

        authorization.update_to_person(person)

    elif mode == auth.AUTHORIZATION_ADMINISTRATOR:
        admin = container.services.auth.administrator_with_token(token)

        if not admin:
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )
            return jsonify(dict()), 401

        authorization.update_to_administrator(admin)

    else:
        logger.info(
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )

        return jsonify(dict()), 401


def auth_manager():
    authorization = container.authorization

    if authorization.is_person() and authorization.person.is_account_manager():
        return

    return jsonify(dict()), 401


def validate(*path):
    schema = current_app.extensions['jsonschema'].get_schema(path)
    try:
        jsonschema.validate(request.json, schema)
    except jsonschema.ValidationError:
        # TODO build JSON-API compliant error responses
        return jsonify(dict()), 422
