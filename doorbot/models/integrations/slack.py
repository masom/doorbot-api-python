# -*- coding: utf-8 -*-
from slacker import Slacker
from .integration import IntegrationInterface
from ...core.model import JobStatuses


class Slack(IntegrationInterface):
    properties = [
        'token', 'room', 'server', 'group_channel'
    ]

    name = "slack"
    title = "Slack"
    description = "Messaging app for teams"
    url = "https://slack.com/"

    can_notify_group = True
    can_notify_users = True
    can_sync_users = True

    def can_notify_user(self, notification):
        if not self.can_notify_users or not notification.user_id:
            return False

        return self.get_service_user(notification) or False

    def can_notify_group(self, notification):
        return self.can_notify_group and len(self.group_channel) > 0

    def notify_user(self, notification, delivery):
        message = "Hello {name}," \
                  "someone is waiting at the {door_name} door.".format(
                      name=notification.person.name,
                      door_name=notification.door.name
                  )

        slacker = Slacker(self.token)
        response = slacker.im.open(
            user=self.get_service_user(notification).service_user_id
        )

        if not response.successful:
            delivery.status = JobStatuses.FAILED
            delivery.response = response.raw
            return

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
        response = slacker.chat.post_message(
            channel=self.group_channel, text=message, username="Doorbot"
        )

        if not response.successful:
            delivery.status = JobStatuses.FAILED
            delivery.response = response.raw
        else:
            delivery.status = JobStatuses.SUCCESS
            delivery.response = response.raw
