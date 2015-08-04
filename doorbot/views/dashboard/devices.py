from flask import Blueprint, render_template, abort, url_for, redirect
from ...container import container
from ...middlewares import auth_manager
from .middlewares import s

devices = Blueprint('devices', __name__, url_prefix='/devices')


def index():
    return render_template(
        'devices/index.html',
        devices=container.account.devices.all()
    )


def create():
    form = ''
    return render_template('devices/create.html', form=form)


def update(id):
    form = ''
    return render_template('devices/update.html', form=form)


def delete(id):
    device = container.account.devices.filter_by(id=id).first()
    if not device:
        abort(404)

    container.database.remove(device)
    container.database.commit()

    return redirect(url_for('.index'))


devices.add_url_rule(
    '', 'index',
    s(auth_manager, index),
    methods=['GET']
)

devices.add_url_rule(
    '/new', 'new',
    s(auth_manager, create),
    methods=['GET', 'POST']
)

devices.add_url_rule(
    '/<int:id>/edit', 'edit',
    s(auth_manager, update),
    methods=['GET', 'POST']
)

devices.add_url_rule(
    '/<int:id>/delete',
    'delete',
    s(auth_manager, delete),
    methods=['GET', 'POST']
)
