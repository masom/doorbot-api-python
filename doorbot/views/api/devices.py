from flask import Blueprint, jsonify, request
from ...middlewares import(
    s, auth_manager
)
from ...container import container
from structlog import get_logger

logger = get_logger()

devices = Blueprint('devices', __name__, url_prefix='/api/devices')


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
    '', 'index', s(auth_manager, index), methods=['GET']
)

devices.add_url_rule(
    '', 'create', s(auth_manager, create), methods=['POST']
)

devices.add_url_rule(
    '/<int:id>', 'view',
    s(auth_manager, view),
    methods=['GET']
)

devices.add_url_rule(
    '/<int:id>', 'update',
    s(auth_manager, update),
    methods=['PUT']
)

devices.add_url_rule(
    '/<int:id>', 'delete',
    s(auth_manager, delete),
    methods=['DELETE']
)
