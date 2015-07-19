from flask import Blueprint, jsonify, request
from ...middlewares import (
    m, auth_secured, auth_manager, validate
)
from ...container import container


people = Blueprint('people', __name__, url_prefix='/api/people')


class PublicPerson(object):
    def __init__(self, id, name, email, is_available):
        self.id = id
        self.name = name
        self.email = email
        self.is_available = is_available

    def to_dict(self):
        return dict(
            id=self.id, name=self.name, email=self.email,
            is_available=self.is_available
        )

    @classmethod
    def from_person(cls, person):
        return cls(
            id=person.id,
            name=person.name,
            email=person.email,
            is_available=person.is_available
        )


def index():
    people = container.repositories.people.all()

    authorization = container.authorization

    if authorization.is_administrator():
        return jsonify(dict(people=people))

    return jsonify(dict(
        people=[
            PublicPerson.from_person(person).to_dict()
            for person in people
        ]
    ))


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
    '', 'create',
    m(validate('person_create'), create),  # auth_secured, auth_manager,
    methods=['POST']
)

people.add_url_rule(
    '/<int:id>', 'view',
    m(auth_secured, view),
    methods=['GET']
)

people.add_url_rule(
    '/<int:id>', 'update',
    m(auth_secured, validate('person_update'), update),
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
