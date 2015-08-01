# -*- coding: utf-8 -*-
from slacker import Slacker
from .integration import IntegrationInterface
from ..service_user import ServiceUser
from ...core.model import JobStatuses
from structlog import get_logger
logger = get_logger()


class Slack(IntegrationInterface):
    properties = [
        'token', 'server', 'group_channel',
        'incoming_webhook_url'
    ]

    name = "slack"
    title = "Slack"
    description = "Messaging app for teams"
    url = "https://slack.com/"

    can_notify_group = True
    can_notify_users = True
    can_sync_users = True

    def can_notify_users(self, notification):
        if not self.can_notify_users or not notification.user_id:
            return False

        return self.get_service_user(notification) or False

    def can_notify_groups(self, notification):
        return self.can_notify_group and len(self.group_channel) > 0

    def can_fetch_users(self):
        return self.can_fetch_users and len(self.token) > 0

    def fetch_users(self):
        slacker = Slacker(self.token)
        response = slacker.users.list()
        if not response.ok:
            logger.warning(
                'Slack fetch_users failed',
                response=response.raw,
                integration_id=self.integration.id
            )
            return False

        users = []

        for member in response.body['members']:
            if member['deleted']:
                continue

            user = ServiceUser()
            user.integration_id = self.integration.id
            user.service = self.name
            user.name = member['profile']['real_name']
            user.email = member['profile']['email']
            user.phone_number = member['profile']['phone_number']
            users.append(user)

        return users

    def notify_user(self, notification, delivery):
        message = "Hello {name}," \
                  "someone is waiting at the {door_name} door.".format(
                      name=notification.person.name,
                      door_name=notification.door.name
                  )

        slacker = Slacker(self.token)

        data = dict(
            username="Doorbot",
            payload=message,
            channel="@{channel}".format(
                channel=self.get_service_user(notification).service_user_id
            )
        )

        response = slacker.incomingwebhook.post(data)

        if not response.successful:
            delivery.status = JobStatuses.FAILED
            delivery.response = response.raw
            return False

        id = response.body['channel']['id']

        response = slacker.chat.post_message(
            channel=id, text=message, username="Doorbot"
        )

        if not response.successful:
            delivery.status = JobStatuses.FAILED
            delivery.response = response.raw
        else:
            delivery.status = JobStatuses.SUCCESS
            delivery.response = response.raw

    def notify_group(self, notification, delivery):
        message = "Hello, someone is waiting at the {door_name} door.".format(
            door_name=notification.door.name
        )

        slacker = Slacker(self.token)
        data = dict(
            username="Doorbot",
            payload=message,
            channel="@{channel}".format(
                channel=self.group_channel
            )
        )

        response = slacker.incomingwebhook.post(data)

        if not response.successful:
            delivery.status = JobStatuses.FAILED
            delivery.response = response.raw
        else:
            delivery.status = JobStatuses.SUCCESS
            delivery.response = response.raw

    @classmethod
    def fields(cls):
        return [
            dict(
                name='incoming_webhook_url', type='url',
                placeholder='Incoming webhook url',
                required=False
            ),
            dict(
                name='group_channel', type='text',
                placeholder='Group channel',
                required=False
            ),
            dict(
                name='token', type='text',
                placeholder='User token',
                required=False
            )
        ]
