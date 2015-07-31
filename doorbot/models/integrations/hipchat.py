# -*- coding: utf-8 -*-
from .integration import IntegrationInterface
import json
import requests
from ...core.model import JobStatuses


class HipChat(IntegrationInterface):
    properties = [
        'token', 'room'
    ]

    name = 'hipchat'
    title = 'HipChat'
    description = 'Private group chat'
    url = 'https://www.hipchat.com/'

    can_notify_group = True
    can_notify_users = True
    can_sync_users = True

    def can_notify_user(self, notification):
        if not self.can_notify_users or notification.user is None:
            return False

        return self.get_service_user(notification) or False

    def notify_user(self, notification, delivery):
        message = dict(
            message='Hello {name}. Someone is waiting for you at the'
                    '{door_name} door'.format(
                        name=notification.person.name,
                        door_name=notification.door.name
                    ),
            notify=True,
            message_format='text'
        )

        hipchat_user = self.get_service_user(notification)
        if not hipchat_user:
            delivery.status = JobStatuses.FAILED
            return

        headers = {
            'Authorization': 'Bearer {token}'.format(token=self.token),
            'Content-Type': 'application/json'
        }

        response = requests.post(
            'https://api.hipchat.com/v2/users/{user_id}/message'.format(
                user_id=hipchat_user.service_user_id
            ),
            data=json.dumps(message),
            headers=headers
        )

        delivery.response = response.body

        if not response.status == requests.STATUS_OK:
            delivery.status = JobStatuses.FAILED
        else:
            delivery.status = JobStatuses.SUCCESS

    def notify_group(self, notification, delivery):
        message = dict(
            message='Hello, Someone is waiting at the {door_name} door.'
                    .format(door_name=notification.door.name),
            notify=True,
            message_format='text'
        )

        headers = {
            'Authorization': 'Bearer {token}'.format(token=self.token),
            'Content-Type': 'application/json'
        }

        response = requests.post(
            'https://api.hipchat.com/v2/room/{room}/notification'.format(
                room=self.room
            ),
            data=json.dumps(message),
            headers=headers
        )

        delivery.response = response.body
        if not response.status == requests.STATUS_OK:
            delivery.status = JobStatuses.FAILED
        else:
            delivery.status = JobStatuses.SUCCESS

    def fetch_users(self):
        return []

    @classmethod
    def fields(cls):
        return [
            dict(
                name='token', type='text',
                placeholder='HipChat V2 API token',
                required=True
            ),
            dict(
                name='room', type='text',
                placeholder='Optional room to broadcast events'
            ),
        ]
