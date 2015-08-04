from flask import Blueprint
from ...container import container
from ...middlewares.dashboard import (auth_manager, render, s)

doors = Blueprint('doors', __name__, url_prefix='/doors')


def index():
    return dict(
        doors=container.account.doors.all()
    )


def create():
    return dict()


def update(id):
    return dict()


def delete(id):
    return dict()

doors.add_url_rule(
    '', 'index',
    s(auth_manager, index, render('doors/index.html')),
    methods=['GET']
)

doors.add_url_rule(
    '/new', 'new',
    s(auth_manager, create, render('doors/create.html')),
    methods=['GET', 'POST']
)

doors.add_url_rule(
    '/<int:id>/edit', 'edit',
    s(auth_manager, update, render('doors/update.html')),
    methods=['GET', 'POST']
)

doors.add_url_rule(
    '/<int:id>/delete',
    'delete',
    s(auth_manager, delete, render('doors/delete.html')),
    methods=['GET', 'POST']
)
