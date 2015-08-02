# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ...container import container
from ...middlewares import (
    s, auth_owner, validate
)
from .view_models import PublicAccount, Account as AccountViewModel

account = Blueprint('account', __name__, url_prefix='/api/account')


def view():
    account = container.account
    authorization = container.authorization

    if authorization.is_administrator():
        return dict(
            account=AccountViewModel.from_account(account)
        )

    if authorization.is_person():
        if authorization.person.is_account_manager():
            return dict(
                account=AccountViewModel.from_account(account)
            )
        else:
            return dict(
                account=PublicAccount.from_account(account)
            )

    return dict(), 403


def update():
    json = request.get_json()
    account = container.account

    account.contact_name = json['account'].get(
        'contact_name', account.contact_name
    )
    account.contact_phone_number = json['account'].get(
        'contact_phone_number',
        account.contact_phone_number
    )
    account.contact_email = json['account'].get(
        'contact_email',
        account.contact_email
    )

    synchronize_people_with_integration_id = json['account'].get(
        'synchronize_people_with_integration_id',
        account.synchronize_people_with_integration_id
    )

    if synchronize_people_with_integration_id > 0:
        integration = account.integrations.filter_by(
            id=synchronize_people_with_integration_id
        ).first()

        if integration:
            account.synchronize_people_with_integration_id = integration.id
        else:
            return dict(), 400

    container.database.commit()

    return dict(
        account=AccountViewModel.from_account(account)
    )

account.add_url_rule(
    '', 'view', s(view),
    methods=['GET']
)

account.add_url_rule(
    '', 'update',
    s(auth_owner, validate('account_update'), update),
    methods=['PUT']
)
