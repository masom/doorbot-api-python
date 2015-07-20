# -*- coding: utf-8 -*-

from .integration import Integration


class Nexmo(Integration):
    __properties__ = [
        'token'
    ]

    name = "nexmo"
    title = "Nexmo"

    can_notify_group = False
    can_notify_users = True
    can_sync_users = False
