from flask import Blueprint, jsonify, request
from ..container import container
from ..security.policies import get_policy_for_person


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/password', methods=['POST'])
def password():
    result = container.services.auth.person_with_password(
        request.data.password
    )

    if result.get('error', False):
        pass

    return jsonify(dict(
        authentication=dict(
            token="{person_id}.{token}".format(
                person_id=result.person.id,
                token=result.auth.token
            )
        ),
        person=result.person,
        policy=get_policy_for_person(result.person)
    ))
