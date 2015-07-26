from flask import (
    abort, Blueprint, request, render_template, redirect, url_for
)
from ...models import Account
from ...db import db
from .forms import AccountCreateForm, AccountUpdateForm


accounts = Blueprint('accounts', __name__, url_prefix='/accounts')


def index():
    return render_template(
        'accounts/index',
        accounts=db.query(Account).filter_by(is_deleted=False).all()
    )


def create():
    form = AccountCreateForm(request.form)

    if request.method == 'POST' and form.validate():
        account = Account()
        account.contact_name = form.contact_name.data
        account.contact_email = form.contact_email.data

        db.add(account)
        db.commit()

        return redirect(url_for('.index'))

    return render_template(
        'accounts/create',
        form=form
    )


def update(id):

    account = db.query(Account).filter_by(id=id).first()

    if not account:
        return abort(404)

    form = AccountUpdateForm(request.form)
    if request.method == 'POST' and form.validate():
        account.contact_name = form.contact_name.data

        db.commit()

    return render_template(
        'accounts/update',
        form=form
    )

accounts.add_url_rule(
    '', 'index', index,
    methods=['GET']
)

accounts.add_url_rule(
    '', 'create', create,
    methods=['POST']
)

accounts.add_url_rule(
    '/<int:id>', 'update', update,
    methods=['PUT']
)
