# -*- coding: utf-8 -*-

from .integration import IntegrationInterface


class Nexmo(IntegrationInterface):
    properties = [
        'token'
    ]

    name = "nexmo"
    title = "Nexmo"

    can_notify_group = False
    can_notify_people = True
    can_sync_people = False
