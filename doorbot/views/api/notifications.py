# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request
from ..midlewares import(
    s, validate
)
from ...container import container


notifications = Blueprint(
    'notifications', __name__, prefix='/api/notifications'
)


def notify():
    account = container.account
    person = account.people.filter_by(id=request.data.person_id).first()
    door = account.doors.filter_by(id=request.data.door_id).first()

    if not door:
        return dict(), 422

    if not person:
        return dict(), 422

    container.services.notifications.knock_knock(person, door)

    return jsonify(dict()), 204


notifications.add_url_rule(
    '/notify', 'notify',
    s(validate('notifications_notify'), notify),
    methods=['POST']
)
