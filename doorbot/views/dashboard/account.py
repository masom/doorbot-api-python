from flask import Blueprint, render_template
from ...middlewares import auth_manager
from .middlewares import s

from ...container import container

account = Blueprint('account', __name__, url_prefix='/account')


def view():
    account = container.account
    return render_template('accounts/view.html', account=account)


def update():
    account = container.account
    return render_template('accounts/view.html', account=account)

account.add_url_rule(
    '', 'view',
    s(view),
    methods=['GET']
)

account.add_url_rule(
    '/edit', 'update',
    s(auth_manager),
    methods=['GET', 'POST']
)
