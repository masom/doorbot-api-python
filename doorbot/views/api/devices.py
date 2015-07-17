from flask import Blueprint, jsonify, request
from ..midlewares import(
    m, auth_secured, auth_manager
)
from ...container import container
import logging

logger = logging.getLogger(__name__)

devices = Blueprint('devices', __name__, url_prefix='/devices')


def index():
    devices = container.repositories.devices.all()

    return jsonify(dict(devices=devices))


def view(id):

    device = container.repositories.devices.first(id=id)

    if not device:
        pass

    return jsonify(dict(device=device))


def create():
    devices = container.repositories.devices

    device = devices.new()
    device.name = request.data.name

    devices.save(device)

    return jsonify(dict(device=device)), 204


def update(id):
    devices = container.repositories.devices

    device = devices.first(id=id)

    if not device:
        return jsonify(dict()), 404

    device.name = request.data.name
    device.door_id = request.data.door_id

    devices.save(device)

    return jsonify(dict(device=device))


def delete(id):

    device = container.repositories.devices

    if not device:
        pass

    devices.delete(device)

    return jsonify(dict()), 200


devices.add_url_rule(
    '', 'index', m(auth_secured, auth_manager, index), methods=['GET']
)

devices.add_url_rule(
    '', 'create', m(auth_secured, auth_manager, create), methods=['POST']
)

devices.add_url_rule(
    '/<int:id>', 'view',
    m(auth_secured, auth_manager, view),
    methods=['GET']
)

devices.add_url_rule(
    '/<int:id>', 'update',
    m(auth_secured, auth_manager, update),
    methods=['PUT']
)

devices.add_url_rule(
    '/<int:id>', 'delete',
    m(auth_secured, auth_manager, delete),
    methods=['DELETE']
)
