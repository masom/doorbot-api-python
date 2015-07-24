# -*- coding: utf-8 -*-

from flask import Blueprint
from ...container import container
from ...middlewares import (
    s, auth_owner, validate
)
from .view_models import PublicAccount, Account as AccountViewModel

bp = Blueprint('account', __name__, url_prefix='/api/account')


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

    account = container.account

    if not account:
        pass

    container.database.commit()

    return dict(
        account=AccountViewModel.from_account(account)
    )

bp.add_url_rule(
    '', 'view', s(view),
    methods=['GET']
)

bp.add_url_rule(
    '', 'update',
    s(auth_owner, validate('account_update'), update),
    methods=['PUT']
)
