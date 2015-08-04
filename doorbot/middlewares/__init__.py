# -*- coding: utf-8 -*-

from flask import request
from ..container import container
from ..models import Account
from .. import auth
import uuid
from structlog import get_logger

log = get_logger()


def _log_unauthorized_access(**context):
    context['module'] = __name__
    log.info("unauthorized access", context=context)


def _logger_context():
    log.new(
        request_id=str(uuid.uuid4()),
    )


def account_scope(*args, **kwargs):
    account = container.database.query(Account).filter_by(
        host=request.environ['DOORBOT_ACCOUNT_HOST']
    ).first()
    if not account:
        return dict(), 404

    container.set_account(account)


def auth_admin(*args, **kwargs):
    if container.authorization.is_administrator():
        return

    return dict(), 403


def auth_gatekeeper():
    pass


def auth_owner(*args, **kwargs):
    authorization = container.authorization

    if authorization.is_person() and authorization.person.is_account_owner():
        return

    return dict(), 403


def auth_secured(*args, **kwargs):
    (mode, token) = auth.parse_token_authorization(
        request.headers.get('Authorization', None)
    )

    if not mode or not token:
        return dict(), 401

    authorization = container.authorization
    if mode == auth.AUTHORIZATION_DEVICE:
        device = container.services.auth.device_with_token(token)
        if not device:
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )

            return dict(), 401

        authorization.update_to_device(device)

    elif mode == auth.AUTHORIZATION_PERSON:
        person = container.services.auth.person_with_token(token)
        if not person:
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )

            return dict(), 401

        authorization.update_to_person(person)

    elif mode == auth.AUTHORIZATION_ADMINISTRATOR:
        admin = container.services.auth.administrator_with_token(token)

        if not admin:
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )
            return dict(), 401

        authorization.update_to_administrator(admin)

    else:
        log.info(
            _log_unauthorized_access(
                method="auth_secured", mode=mode, token=token,
                account_id=container.account.id
            )
        )

        return dict(), 401


def auth_manager(*args, **kwargs):
    authorization = container.authorization

    if authorization.is_person() and authorization.person.is_account_manager():
        return

    return dict(), 401
