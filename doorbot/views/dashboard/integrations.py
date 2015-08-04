from flask import Blueprint
from ...container import container
from ...middlewares.dashboard import (auth_manager, render, s)

integrations = Blueprint('integrations', __name__, url_prefix='/integrations')


def index():
    return dict(
        integrations=container.account.integrations.all()
    )


def create():
    return dict()


def update(id):
    return dict()


def delete(id):
    return dict()

integrations.add_url_rule(
    '', 'index',
    s(auth_manager, index, render('integrations/index.html')),
    methods=['GET']
)

integrations.add_url_rule(
    '/new', 'new',
    s(auth_manager, create, render('integrations/create.html')),
    methods=['GET', 'POST']
)

integrations.add_url_rule(
    '/<int:id>/edit', 'edit',
    s(auth_manager, update, render('integrations/update.html')),
    methods=['GET', 'POST']
)

integrations.add_url_rule(
    '/<int:id>/delete',
    'delete',
    s(auth_manager, delete, render('integrations/delete.html')),
    methods=['GET', 'POST']
)
