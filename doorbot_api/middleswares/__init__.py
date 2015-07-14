# -*- coding: utf-8 -*-

from flask import jsonify, request
from ..container import container
from .. import auth


def m(*args):

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
            return jsonify(dict()), 401

        authorization.update_to_device(device)

    elif mode == auth.AUTHORIZATION_PERSON:
        person = container.services.auth.person_with_token(token)
        if not person:
            return jsonify(dict()), 401

        authorization.update_to_person(person)

    elif mode == auth.AUTHORIZATION_ADMINISTRATOR:
        admin = container.services.auth.administrator_with_token(token)

        if not admin:
            return jsonify(dict()), 401

        authorization.update_to_administrator(admin)
    else:
        return jsonify(dict()), 401


def auth_manager():
    authorization = container.authorization

    if authorization.is_person() and authorization.person.is_account_manager():
        return

    return jsonify(dict()), 401
