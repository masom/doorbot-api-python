from flask import Blueprint, render_template, abort, url_for, redirect
from ...container import container
from ...middlewares import auth_manager
from .middlewares import s

doors = Blueprint('doors', __name__, url_prefix='/doors')


def index():
    return render_template(
        'doors/index.html',
        doors=container.account.doors.all()
    )


def create():
    form = ''
    return render_template('doors/index.html', form=form)


def view(id):
    door = container.account.doors.filter_by(id=id).first()
    if not door:
        abort(404)

    return render_template('doors/view.html', door=door)


def update(id):
    door = container.account.doors.filter_by(id=id).first()
    if not door:
        abort(404)

    form = ''
    return render_template('doors/update.html', door=door, form=form)


def delete(id):
    door = container.account.doors.filter_by(id=id).first()
    if not door:
        abort(404)

    return redirect(url_for('.index'))

doors.add_url_rule(
    '', 'index',
    s(auth_manager, index, ),
    methods=['GET']
)

doors.add_url_rule(
    '/new', 'new',
    s(auth_manager, create),
    methods=['GET', 'POST']
)

doors.add_url_rule(
    '/<int:id>/edit', 'edit',
    s(auth_manager, update),
    methods=['GET', 'POST']
)

doors.add_url_rule(
    '/<int:id>/delete',
    'delete',
    s(auth_manager, delete),
    methods=['GET', 'POST']
)
