from flask import Blueprint
from ...container import container
from ...middlewares.dashboard import (auth_manager, render, s)

devices = Blueprint('devices', __name__, url_prefix='/devices')


def index():
    return dict(
        devices=container.account.devices.all()
    )


def create():
    return dict()


def update(id):
    return dict()


def delete(id):
    return dict()

devices.add_url_rule(
    '', 'index',
    s(auth_manager, index, render('devices/index.html')),
    methods=['GET']
)

devices.add_url_rule(
    '/new', 'new',
    s(auth_manager, create, render('devices/create.html')),
    methods=['GET', 'POST']
)

devices.add_url_rule(
    '/<int:id>/edit', 'edit',
    s(auth_manager, update, render('devices/update.html')),
    methods=['GET', 'POST']
)

devices.add_url_rule(
    '/<int:id>/delete',
    'delete',
    s(auth_manager, delete, render('devices/delete.html')),
    methods=['GET', 'POST']
)
