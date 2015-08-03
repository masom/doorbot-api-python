# -*- coding: utf-8 -*-
from slacker import Slacker, Response
import requests
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
    can_notify_people = True
    can_sync_people = True

    def fetch_people(self):
        slacker = Slacker(self.token)
        response = slacker.users.list()
        if not response.successful:
            logger.warning(
                'Slack fetch_users failed',
                response=response.raw,
                integration_id=self.integration.id,
                account_id=self.integration.account_id
            )
            return False

        users = []

        for member in response.body['members']:
            if member['deleted']:
                continue

            if member['profile'].get('bot_id', False):
                continue

            if not member['profile'].get('email', False):
                continue

            user = ServiceUser()
            user.integration_id = self.integration.id
            user.service = self.name
            user.name = member['profile']['real_name']
            user.email = member['profile']['email']
            user.phone_number = member['profile'].get('phone_number')
            user.service_user_id = member['id']
            user.extra['username'] = member['name']
            users.append(user)

        logger.info(
            'Slack fetch_users completed',
            count=len(users),
            account_id=self.integration.account_id,
            integration_id=self.integration.id
        )
        return users

    def notify_person(self, notification, delivery):
        message = "Hello {name}," \
                  "someone is waiting at the {door_name} door.".format(
                      name=notification.person.name,
                      door_name=notification.door.name
                  )

        slacker = Slacker(
            token=self.token, incoming_webhook_url=self.incoming_webhook_url
        )

        username = self.get_service_user(notification).extra.get(
            'username', None
        )

        if not username:
            delivery.status = JobStatuses.FAILED
            return False

        data = dict(
            username="Doorbot",
            text=message,
            channel="@{channel}".format(
                channel=username
            )
        )

        logger.info('derp', data=data)

        response = slacker.incomingwebhook.post(data)

        logger.debug(
            'slack webhook response',
            response_status_code=response.status_code,
            response_text=response.text
        )

        if not response.status_code == requests.STATUS_OK:
            delivery.status = JobStatuses.FAILED
            delivery.response = response.raw
        else:
            delivery.status = JobStatuses.SUCCESS
            delivery.response = response.raw

    def notify_group(self, notification, delivery):
        message = "Hello, someone is waiting at the {door_name} door.".format(
            door_name=notification.door.name
        )

        slacker = Slacker(
            token=self.token, incoming_webhook_url=self.incoming_webhook_url
        )
        data = dict(
            username="Doorbot",
            payload=message,
            channel="@{channel}".format(
                channel=self.group_channel
            )
        )

        response = Response(slacker.incomingwebhook.post(data))

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
