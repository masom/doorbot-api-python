from flask import Blueprint
from ...container import container
from ...middlewares.dashboard import (auth_manager, render, s)

people_authentications = Blueprint(
    'people_authentications', __name__, url_prefix='/people'
)


def index():
    return dict(
        people_authentications=container.account.people_authentications.all()
    )


def create(person_id):
    return dict()


def update(person_id, id):
    return dict()


def delete(person_id, id):
    return dict()


people_authentications.add_url_rule(
    '/authentications', 'index',
    s(auth_manager, index, render('people_authentications/index.html')),
    methods=['GET']
)

people_authentications.add_url_rule(
    '/<int:person_id>/authentications/new', 'new',
    s(create, render('people_authentications/create.html')),
    methods=['GET', 'POST']
)

people_authentications.add_url_rule(
    '/<int:person_id>/authentications/<int:id>/edit', 'edit',
    s(update, render('people_authentications/update.html')),
    methods=['GET', 'POST']
)

people_authentications.add_url_rule(
    '/<int:person_id>/authentications/<int:id>/delete',
    'delete',
    s(delete, render('people_authentications/delete.html')),
    methods=['GET', 'POST']
)
