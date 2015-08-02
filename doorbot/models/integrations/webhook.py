# -*- coding: utf-8 -*-
import requests
from ...core.model import JobStatuses
from .integration import IntegrationInterface
from structlog import get_logger
logger = get_logger()


class Webhook(IntegrationInterface):
    properties = [
        'url'
    ]

    name = "webhook"
    title = "webhook"
    description = "Webhook"
    url = "https://doorbot.co/docs/webhook"

    allow_multiple = True
    can_notify_group = True
    can_notify_users = True
    can_sync_users = False

    def notify_user(self, notification, delivery):
        return self._send(notification, delivery)

    def notify_group(self, notification, delivery):
        return self._send(notification, delivery)

    def _send(self, notification, delivery):
        headers = {
            'Content-Type': 'application/json'
        }

        data = dict(
            account=dict(
                host=notification.account.host
            ),
            notification=dict(
                id=notification.id,
                created_at=notification.created_at
            ),
            door=dict(
                id=notification.door.id,
                name=notification.door.name
            ),
            person=dict(
                id=notification.person.id,
                name=notification.person.name
            )
        )

        try:
            response = requests.post(
                self.url, data=data, headers=headers, timeout=(3.0, 3.0),
                allow_redirects=False
            )
        except (requests.TimeoutException, requests.TooManyRedirects):
            logger.info(
                'Webhook timeout or too many redirects',
                account_id=notification.account_id,
                notification_id=notification.id,
                door_id=notification.door.id,
                person_id=notification.person.id
            )
            delivery.status = JobStatuses.ERROR
            return

        delivery.response = response.body

        if response.status == requests.STATUS_OK:
            delivery.status = JobStatuses.SUCCESS
        else:
            delivery.status = JobStatuses.FAILED

    @classmethod
    def fields(cls):
        return [
            dict(
                name="url", type="url",
                placeholder="HTTP URL",
                required=True
            )
        ]
