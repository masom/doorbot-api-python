from flask import Blueprint, render_template
from ...container import container
from ...middlewares import auth_manager
from .middlewares import s

people = Blueprint('people', __name__, url_prefix='/people')


def index():
    return render_template(
        'people/index.html',
        people=container.account.people.all()
    )


def create():
    return render_template('people/create.html')


def update(id):
    return render_template('people/update.html')


def delete(id):
    return render_template('people/delete.html')


people.add_url_rule(
    '', 'index',
    s(auth_manager, index),
    methods=['GET']
)

people.add_url_rule(
    '/new', 'new',
    s(auth_manager, create),
    methods=['GET', 'POST']
)

people.add_url_rule(
    '/<int:id>/edit', 'edit',
    s(auth_manager, update),
    methods=['GET', 'POST']
)

people.add_url_rule(
    '/<int:id>/delete',
    'delete',
    s(auth_manager, delete),
    methods=['GET', 'POST']
)
