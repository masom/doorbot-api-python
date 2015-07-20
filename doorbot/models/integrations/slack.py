# -*- coding: utf-8 -*-

from .integration import Integration


class Slack(Integration):
    __properties__ = [
        'token', 'room', 'server'
    ]

    name = "slack"
    title = "Slack"
    description = "Messaging app for teams"
    url = "https://slack.com/"

    can_notify_group = True
    can_notify_users = True
    can_sync_users = True
