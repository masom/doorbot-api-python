# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ...middlewares import auth_manager
from .middlewares import (s, validate)
from ...models import Door
from ...container import container
from .view_models import Door as DoorViewModel


doors = Blueprint(
    'doors', __name__, url_prefix='/doors'
)


def index():
    doors = container.account.doors.all()

    return dict(doors=[DoorViewModel.from_door(door) for door in doors])


def view(id):

    door = container.account.doors.filter_by(id=id, is_deleted=False).first()

    if not door:
        return dict(), 404

    return dict(door=DoorViewModel.from_door(door))


def create():
    json = request.get_json()

    doors = container.account.doors

    door = Door()
    door.name = json['door']['name']
    doors.append(door)

    container.database.commit()

    return dict(door=DoorViewModel.from_door(door)), 201


def update(id):
    door = container.account.doors.filter_by(id=id, is_deleted=False).first()

    if not door:
        return dict(), 404

    door.name = request.data.name
    container.database.commit()

    return dict(door=DoorViewModel.form_door(door))


def delete(id):

    door = container.account.doors.filter_by(id=id, is_deleted=False).first()

    if not door:
        return dict(), 404

    container.database.delete(door)
    container.database.commit()

    return dict(), 200


doors.add_url_rule(
    '', 'index', s(auth_manager, index), methods=['GET']
)

doors.add_url_rule(
    '', 'create',
    s(auth_manager, validate('door_create'), create),
    methods=['POST']
)

doors.add_url_rule(
    '/<int:id>', 'view',
    s(auth_manager, view),
    methods=['GET']
)

doors.add_url_rule(
    '/<int:id>', 'update',
    s(auth_manager, validate('door_update'), update),
    methods=['PUT']
)

doors.add_url_rule(
    '/<int:id>', 'delete',
    s(auth_manager, delete),
    methods=['DELETE']
)
