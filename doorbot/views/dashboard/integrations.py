from flask import Blueprint, render_template, abort, url_for, redirect
from ...container import container
from ...middlewares import auth_manager
from .middlewares import s

integrations = Blueprint('integrations', __name__, url_prefix='/integrations')


def index():
    return render_template(
        'integrations/index.html',
        integrations=container.account.integrations.all()
    )


def create():
    form = ''
    return render_template('integrations/create.html', form=form)


def update(id):
    integration = container.account.integrations.filter_by(id=id).first()
    if not integration:
        abort(404)

    form = ''
    return render_template(
        'integrations/update.html', integration=integration, form=form
    )


def delete(id):
    integration = container.account.integrations.filter_by(id=id).first()
    if not integration:
        abort(404)

    return redirect(url_for('.index'))


integrations.add_url_rule(
    '', 'index',
    s(auth_manager, index),
    methods=['GET']
)

integrations.add_url_rule(
    '/new', 'new',
    s(auth_manager, create),
    methods=['GET', 'POST']
)

integrations.add_url_rule(
    '/<int:id>/edit', 'edit',
    s(auth_manager, update),
    methods=['GET', 'POST']
)

integrations.add_url_rule(
    '/<int:id>/delete',
    'delete',
    s(auth_manager, delete),
    methods=['GET', 'POST']
)
