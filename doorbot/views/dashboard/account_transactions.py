from flask import Blueprint, abort, render_template
from ...middlewares import auth_manager
from .middlewars import s
from ...container import container


account_transactions = Blueprint(
    'account_transactions', __name__, url_prefix='/account/transactions'
)


def index():
    account = container.account
    return dict(transactions=account.transactions.all())


def view(id):
    account = container.account
    transaction = account.transactions.filter_by(id=id).first()

    if not transaction:
        abort(404)

    return render_template(
        'account_transactions/view.html',
        transaction=transaction
    )


account_transactions.add_url_rule(
    '', 'index',
    s(auth_manager, index, render_template('account_transactions/view.html')),
    methods=['GET']
)

account_transactions.add_url_rule(
    '/<int:id>', 'view',
    s(auth_manager, view),
    methods=['GET']
)
