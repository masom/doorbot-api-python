# -*- coding: utf-8 -*-

import requests
from ...core.model import JobStatuses
from .integration import IntegrationInterface
from structlog import get_logger
logger = get_logger()


class Mailgun(IntegrationInterface):
    properties = [
        'domain', 'token', 'group_email'
    ]

    name = "mailgun"
    title = "Mailgun"
    description = "The Email Service For Developers"
    url = "http://www.mailgun.com/"

    can_notify_group = False
    can_notify_people = True
    can_sync_people = False

    def notify_person(self, notification, delivery):
        return self._send(notification, delivery, notification.person.email)

    def notify_group(self, notification, delivery):
        return self._send(notification, delivery, self.group_email)

    def _send(self, notification, delivery, to):
        url = 'https://api.mailgun.net/v3/{domain}/messages'.format(
            domain=self.domain
        )

        subject = "Someone is waiting for you at the {door_name} door.".format(
            door_name=notification.door.name
        )

        data = {
            "from": "doorbot@doorbot.co",
            "to": to,
            "subject": subject,
            "text": "\n".join(
                "Hello,",
                "Someone is waiting for you at the {door_name} door.".format(
                    door_name=notification.door.name
                )
            )
        }
        # TODO html: render_template...

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(
                url,
                auth=("api", self.token),
                data=data,
                headers=headers,
                timeout=(3.0, 3.0)
            )
        except (requests.TooManyRedirects, requests.Timeout):
            logger.warning(
                'Mailgun timeout or too many redirects',
                account_id=notification.account_id,
                notification_id=notification.id,
                person_id=notification.person_id,
                door_id=notification.door_id
            )
            delivery.status = JobStatuses.ERROR
            return

        if response.status == requests.STATUS_OK:
            delivery.status = JobStatuses.SUCCESS
        else:
            delivery.status = JobStatuses.FAILED

        delivery.response = response.body

    @classmethod
    def fields(self):
        return [
            dict(name="token", type="text", required=True)
        ]
