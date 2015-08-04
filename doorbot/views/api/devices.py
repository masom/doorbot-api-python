from flask import Blueprint, request
from ...middlewares import auth_manager
from .middlewares import (s, validate)
from ...container import container
from ...models import Device
from structlog import get_logger
from .view_models import Device as DeviceViewModel

logger = get_logger()

devices = Blueprint('devices', __name__, url_prefix='/api/devices')


def index():
    devices = container.account.devices.all()

    return dict(devices=devices)


def view(id):

    device = container.account.devices.first(id=id)

    if not device:
        return dict(), 404

    return dict(device=DeviceViewModel.from_device(device))


def create():

    device = Device()
    device.name = request.data.name

    container.account.devices.append(device)
    container.database.commit()

    return dict(device=DeviceViewModel.from_device(device)), 204


def update(id):
    devices = container.account.devices

    device = devices.filter_by(id=id).first()

    if not device or device.is_deleted:
        return dict(), 404

    device.name = request.data.name
    device.door_id = request.data.door_id

    container.database.commit()

    return dict(device=DeviceViewModel.from_device(device))


def delete(id):

    device = container.account.devices.filter_by(id=id).first()

    if not device or device.is_deleted:
        return dict(), 404

    device.is_deleted = True
    container.database.commit()

    return dict(), 200


devices.add_url_rule(
    '', 'index', s(auth_manager, index), methods=['GET']
)

devices.add_url_rule(
    '', 'create',
    s(auth_manager, validate('device_create'), create),
    methods=['POST']
)

devices.add_url_rule(
    '/<int:id>', 'view',
    s(auth_manager, view),
    methods=['GET']
)

devices.add_url_rule(
    '/<int:id>', 'update',
    s(auth_manager, validate('device_update'), update),
    methods=['PUT']
)

devices.add_url_rule(
    '/<int:id>', 'delete',
    s(auth_manager, delete),
    methods=['DELETE']
)
