from flask import Blueprint
from ...middlewars import auth_manager
from .middlewares.dashboard import (
    render, s,
)

from ...container import container

account = Blueprint('account', __name__, url_prefix='account')


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

    return dict(
        account=AccountViewModel.from_account(account)
    )

account.add_url_rule(
    '', 'view',
    s(view, render('account/view.html')),
    methods=['GET']
)

account.add_url_rule(
    '/edit', 'update',
    s(auth_manager, update, render('accounts/update.html')),
    methods=['GET', 'POST']
)
