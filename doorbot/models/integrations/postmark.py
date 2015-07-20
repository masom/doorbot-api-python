# -*- coding: utf-8 -*-

from .integration import Integration


class Postmark(Integration):
    __properties__ = [
        'token'
    ]

    name="postmark"
    title = "Postmark"
    description = "ransactional Email Delivery"
    url = "https://postmarkapp.com/"

    can_notify_group = False
    can_notify_users = True
    can_sync_users = False

    @classmethod
    def fields(cls):
        return [
            dict(name="token", type="text", required=True)
        ]
