from flask import Blueprint, jsonify, request
from ...middlewares import (
    m, auth_secured, auth_manager
)
from ...container import container


people = Blueprint('people', __name__, url_prefix='/people')


def index():
    people = container.repositories.people.all()

    return jsonify(dict(people=people))


def view(id):
    person = container.repositories.people.first(id=id)

    if not person:
        return jsonify(dict()), 404

    return jsonify(dict(person=person))


def create():
    people = container.repositories.people

    person = people.new()
    person.name = request.data.name
    person.title = request.data.title
    person.phone_number = request.data.phone_number

    people.save(person)

    return jsonify(dict(person=person)), 204


def update(id):
    people = container.repositories.people
    person = people.first(id=id)

    if not person.can_be_edited_by(container.authorization):
        return jsonify(dict()), 403

    person.name = request.data.name
    person.phone_number = request.data.phone_number
    person.title = request.data.title

    people.update(person)
    return jsonify(dict(person=person))


def delete(id):

    people = container.repositories.people

    person = people.first(id=id)

    if not person:
        return jsonify(dict()), 404

    people.delete(person)

    return jsonify(dict()), 201


def sync():
    pass


people.add_url_rule(
    '', 'index', m(auth_secured, index), methods=['GET']
)

people.add_url_rule(
    '', 'create', m(auth_secured, auth_manager, create), methods=['POST']
)

people.add_url_rule(
    '/<int:id>', 'view',
    m(auth_secured, view),
    methods=['GET']
)

people.add_url_rule(
    '/<int:id>', 'update',
    m(auth_secured, update),
    methods=['PUT']
)

people.add_url_rule(
    '/<int:id>', 'delete',
    m(auth_secured, auth_manager, delete),
    methods=['DELETE']
)

people.add_url_rule(
    '/sync', 'sync', m(auth_secured, auth_manager, sync), methods=['POST']
)
