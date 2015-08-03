# -*- coding: utf-8 -*-

from .integration import IntegrationInterface


class Postmark(IntegrationInterface):
    properties = [
        'token'
    ]

    name = "postmark"
    title = "Postmark"
    description = "ransactional Email Delivery"
    url = "https://postmarkapp.com/"

    can_notify_group = False
    can_notify_people = True
    can_sync_people = False

    @classmethod
    def fields(cls):
        return [
            dict(name="token", type="text", required=True)
        ]
