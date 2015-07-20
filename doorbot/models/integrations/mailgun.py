# -*- coding: utf-8 -*-

from .integration import Integration


class Mailgun(Integration):
    __properties__ = [
        'token'
    ]

    name = "mailgun"
    title = "Mailgun"
    description = "The Email Service For Developers"
    url = "http://www.mailgun.com/"

    can_notify_group = False
    can_notify_users = True
    can_sync_users = False

    def notify_user(self, notification):
        pass

    @classmethod
    def fields(self):
        return [
            dict(name="token", type="text", required=True)
        ]
