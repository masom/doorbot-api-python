# -*- coding: utf-8 -*-
from .integration import IntegrationInterface


class Webhook(IntegrationInterface):
    properties = [
        'url'
    ]

    name = "webhook"
    title = "webhook"
    description = "Webhook"
    url = ""

    allow_multiple = True
    can_notify_group = True
    can_notify_users = True
    can_sync_users = False

    def notify_user(self, notification):
        pass

    def notify_group(self, notification):
        pass

    @classmethod
    def fields(cls):
        return [
            dict(
                name="url", type="url",
                placeholder="HTTP URL",
                required=True
            )
        ]
