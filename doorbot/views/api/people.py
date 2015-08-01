from flask import Blueprint, request
from ...middlewares import (
    s, auth_manager, validate
)
from ...container import container
from ...models import PeopleSynchronization
from ...jobs import SynchronizePeopleJob
from .view_models import PublicPerson, Person as PersonViewModel

people = Blueprint('people', __name__, url_prefix='/api/people')


def index():
    people = container.account.people.all()

    authorization = container.authorization

    if authorization.is_account_manager():
        return dict(
            people=[PersonViewModel.from_person(person) for person in people]
        )

    return dict(
        people=[
            PublicPerson.from_person(person)
            for person in people
        ]
    )


def view(id):
    person = container.account.people.filter_by(
        id=id, is_deleted=False
    ).first()

    if not person:
        return dict(), 404

    return dict(person=PersonViewModel.from_person(person))


def create():
    people = container.account.people

    person = people.new()
    person.name = request.data.name
    person.title = request.data.title
    person.phone_number = request.data.phone_number

    people.append(person)

    container.database.commit()

    return dict(person=PersonViewModel.from_person(person)), 204


def update(id):
    people = container.account.people
    person = people.filter_by(id=id, is_deleted=False)

    if not person.can_be_edited_by(container.authorization):
        return dict(), 403

    person.name = request.data.name
    person.phone_number = request.data.phone_number
    person.title = request.data.title

    container.database.commit()

    return dict(person=PersonViewModel.from_person(person))


def delete(id):

    people = container.account.people

    person = people.filter_by(id=id, is_deleted=False)

    if not person:
        return dict(), 404

    container.database.delete(person)
    container.database.commit()

    return dict(), 201


def sync():
    sync = PeopleSynchronization()
    container.account.people_synchronizations.append(sync)
    container.database.flush()

    SynchronizePeopleJob().delay(sync.id)

    container.database.commit()

    return dict(), 204


people.add_url_rule(
    '', 'index', s(index), methods=['GET']
)

people.add_url_rule(
    '', 'create',
    s(auth_manager, validate('person_create'), create),
    methods=['POST']
)

people.add_url_rule(
    '/<int:id>', 'view',
    s(view),
    methods=['GET']
)

people.add_url_rule(
    '/<int:id>', 'update',
    s(validate('person_update'), update),
    methods=['PUT']
)

people.add_url_rule(
    '/<int:id>', 'delete',
    s(auth_manager, delete),
    methods=['DELETE']
)

people.add_url_rule(
    '/sync', 'sync', s(auth_manager, sync), methods=['POST']
)
