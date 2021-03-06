# -*- coding: utf-8 -*-

from flask import Blueprint, request
from .middlewares import(
    s, validate
)
from ...container import container
from .view_models import Notification as NotificationViewModel
from ...models import Notification
from structlog import get_logger
from ...jobs import DeliverNotificationJob

logger = get_logger()

notifications = Blueprint(
    'notifications', __name__, url_prefix='/notifications'
)


def create():
    json = request.get_json()

    account = container.account
    person = account.people.filter_by(
        id=json['notification']['person_id'], is_deleted=False
    ).first()

    door = account.doors.filter_by(
        id=json['notification']['door_id'], is_deleted=False
    ).first()

    if not door:
        return dict(), 400

    if not person:
        return dict(), 400

    try:
        notification = Notification(person_id=person.id, door_id=door.id)

        account.notifications.append(notification)

        container.database.flush()

        DeliverNotificationJob().delay(notification.id)

        container.database.commit()

    except Exception as e:
        logger.error(
            'notification failure',
            error=e, account_id=account.id, person_id=person.id,
            door_id=door.id
        )
        container.database.rollback()

        return dict(), 500

    logger.info(
        'notification created',
        account_id=account.id, door_id=door.id, person_id=person.id,
        notification_id=notification.id
    )

    return dict(
        notifiation=NotificationViewModel.from_notification(notification)
    ), 201


notifications.add_url_rule(
    '', 'create',
    s(validate('notifications_create'), create),
    methods=['POST']
)
