# -*- coding: utf-8 -*-

from flask import Blueprint, request
from ...middlewares import(
    s, validate
)
from ...container import container
from .view_models import Notification as NotificationViewModel
from ...models import Notification
from structlog import get_logger

logger = get_logger()

notifications = Blueprint(
    'notifications', __name__, url_prefix='/api/notifications'
)


def create():
    account = container.account
    person = account.people.filter_by(
        id=request.data.person_id, is_deleted=False
    ).first()
    door = account.doors.filter_by(
        id=request.data.door_id, is_deleted=False
    ).first()

    if not door:
        return dict(), 422

    if not person:
        return dict(), 422

    try:
        notification = Notification(person_id=person.id, door_id=door.id)

        account.notifications.append(notification)

        notification.schedule()

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
    ), 204


notifications.add_url_rule(
    '', 'create',
    s(validate('notifications_notify'), create),
    methods=['POST']
)
