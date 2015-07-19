# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from ..midlewares import(
    m, auth_secured
)
from ...container import container


notifications = Blueprint('notifications', __name__, prefix='/api/notifications')


def notify():
    repositories = container.repositories
    person = repositories.people.first(id=request.data.person_id)
    door = repositories.doors.first(id=request.data.door_id)

    if not door:
        pass

    if not person:
        pass

    container.services.notifications.knock_knock(person, door)

    return jsonify(dict()), 204


notifications.add_url_rule(
    '/notify', 'notify',
    m(auth_secured, notify),
    methods=['POST']
)
