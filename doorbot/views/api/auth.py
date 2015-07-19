from flask import Blueprint, request
from ...container import container
from ...security.policies import get_policy_for_person
from ...middlewares import (m, validate)

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


def password():
    result = container.services.auth.person_with_password(
        request.data.password
    )

    if result.get('error', False):
        return dict(), 401

    return dict(
        authentication=dict(
            token="{person_id}.{token}".format(
                person_id=result.person.id,
                token=result.auth.token
            )
        ),
        person=result.person,
        policy=get_policy_for_person(result.person)
    )


def token():
    pass


auth.add_url_rule(
    '/password', 'password',
    m(validate('authentication'), password),
    methods=['POST']
)

auth.add_url_rule(
    '/token', 'token',
    m(validate('authentication'), token),
    methods=['POST']
)
