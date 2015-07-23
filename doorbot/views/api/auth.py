from flask import Blueprint, request
from ...container import container
from ...security.policies import get_policy_for_person
from ...middlewares import (m, account_scope, validate)
from ...auth import AUTHORIZATION_DEVICE, AUTHORIZATION_PERSON
from .view_models import Person as PersonViewModel

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


def password():
    json = request.get_json()
    authentication = json['authentication']

    result = container.services.auth.person_with_password(
        authentication['email'], authentication['password']
    )

    if not result:
        return dict(), 401

    return dict(
        authentication=dict(
            token="{person_id}.{token}".format(
                person_id=result['person'].id,
                token=result['auth'].token
            )
        ),
        person=PersonViewModel.from_person(result['person']),
        policy=get_policy_for_person(result['person'])
    )


def token():
    json = request.get_json()

    authentication = json['authentication']
    if authentication['type'] == AUTHORIZATION_DEVICE:
        result = container.services.auth.device_with_token(
            authentication['token']
        )

        if not result:
            return {}, 401

        return dict(
            device=result
        )

    elif authentication['type'] == AUTHORIZATION_PERSON:
        result = container.services.auth.person_with_token(
            authentication['token']
        )

        if not result:
            return {}, 401

        return dict(
            person=result,
            policy=get_policy_for_person(result)
        )
    else:
        return {}, 401


auth.add_url_rule(
    '/password', 'password',
    m(account_scope, validate('authentication_password'), password),
    methods=['POST']
)

auth.add_url_rule(
    '/token', 'token',
    m(account_scope, validate('authentication_token'), token),
    methods=['POST']
)
