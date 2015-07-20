# -*- coding: utf-8 -*-

from .integration import Integration


class Twilio(Integration):
    __properties__ = [
        'token', 'phone_number'
    ]

    name = "twilio"
    title = "Twilio"
    description = "APIs for Text Messaging, VoIP & Voice in the Cloud"
    url = "https://www.twilio.com/"

    can_notify_group = False
    can_notify_users = True
    can_sync_users = False

    def fields(cls):
        return [
            dict(name="token", type="text", required=True),
            dict(name="phone_number", type="phone", required=True)
        ]
