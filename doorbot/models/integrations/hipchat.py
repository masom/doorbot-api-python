# -*- coding: utf-8 -*-

from .integration import Integration


class HipChat(Integration):
    __properties__ = [
        'token', 'room'
    ]

    name = "hipchat"
    title = "HipChat"
    description = "Private group chat"
    url = "https://www.hipchat.com/"

    can_notify_group = True
    can_notify_users = True
    can_sync_users = True

    def notify_user(self, notification):
        pass

    def notify_group(self, notification):
        pass

    def fetch_users(self):
        return []

    @classmethod
    def fields(cls):
        return [
            dict(
                name="token", type="text",
                placeholder="HipChat V2 API token",
                required=True
            ),
            dict(
                name="room", type="text",
                placeholder="Optional room to broadcast events"
            ),
        ]
