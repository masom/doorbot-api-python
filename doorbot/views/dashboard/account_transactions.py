from flask import Blueprint
from ...middlewares.dashboard import (
    auth_manager
)
from .middlewars import (render, s)
from ...container import container


account_transactions = Blueprint(
    'account_transactions', __name__, url_prefix='/account/transactions'
)


def index():
    account = container.account
    return dict(transactions=account.transactions.all())


def view(id):
    account = container.account
    return dict(transactions=account.transactions.filter_by(id=id).first())


account_transactions.add_url_rule(
    '', 'index',
    s(auth_manager, index, render('account_transactions/view.html')),
    methods=['GET']
)

account_transactions.add_url_rule(
    '/<int:id>', 'view',
    s(auth_manager, view, render('account_transactions/view.html')),
    methods=['GET']
)
