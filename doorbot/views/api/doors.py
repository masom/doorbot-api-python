# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from ..midlewares import(
    s, auth_manager
)
from ...container import container


doors = Blueprint('doors', __name__, url_prefix='/api/doors')


def index():
    doors = container.repositories.doors.all()

    return jsonify(dict(doors=doors))


def view(id):

    door = container.repositories.doors.first(id=id)

    if not door:
        pass

    return jsonify(dict(door=door))


def create():
    doors = container.repositories.doors

    door = doors.new()
    door.name = request.data.name

    doors.save(door)

    return jsonify(dict(door=door)), 204


def update(id):
    doors = container.repositories.doors

    door = doors.first(id=id)

    if not door:
        return jsonify(dict()), 404

    door.name = request.data.name

    doors.save(door)

    return jsonify(dict(door=door))


def delete(id):

    door = container.repositories.doors

    if not door:
        pass

    doors.delete(door)

    return jsonify(dict()), 200


doors.add_url_rule(
    '', 'index', s(auth_manager, index), methods=['GET']
)

doors.add_url_rule(
    '', 'create', s(auth_manager, create), methods=['POST']
)

doors.add_url_rule(
    '/<int:id>', 'view',
    s(auth_manager, view),
    methods=['GET']
)

doors.add_url_rule(
    '/<int:id>', 'update',
    s(auth_manager, update),
    methods=['PUT']
)

doors.add_url_rule(
    '/<int:id>', 'delete',
    s(auth_manager, delete),
    methods=['DELETE']
)
