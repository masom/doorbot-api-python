from flask import Blueprint, render_template, abort, redirect, url_for
from ...container import container
from ...middlewares import auth_manager
from .middlewares import s

people_authentications = Blueprint(
    'people_authentications', __name__, url_prefix='/people'
)


def index():
    return render_template(
        'people_authentications/index.html',
        people_authentications=container.authorization.person.all()
    )


def create():
    form = ''
    return render_template(
        'people_authentications/create.html',
        form=form
    )


def update(id):
    person = container.authorization.person
    authentication = person.authentications.filter_by(id=id).first()

    if not authentication:
        abort(404)

    form = ''
    return render_template(
        'people_authentications/update.html',
        authentication=authentication,
        form=form
    )


def delete(id):

    person = container.authorization.person
    authentication = person.authentications.filter_by(id=id).first()
    if not authentication:
        abort(404)

    return redirect(url_for('.index'))


people_authentications.add_url_rule(
    '/authentications', 'index',
    s(auth_manager, index),
    methods=['GET']
)

people_authentications.add_url_rule(
    '/<int:person_id>/authentications/new', 'new',
    s(create),
    methods=['GET', 'POST']
)

people_authentications.add_url_rule(
    '/<int:person_id>/authentications/<int:id>/edit', 'edit',
    s(update),
    methods=['GET', 'POST']
)

people_authentications.add_url_rule(
    '/<int:person_id>/authentications/<int:id>/delete',
    'delete',
    s(delete),
    methods=['GET', 'POST']
)
