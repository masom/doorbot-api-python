# -*- coding: utf-8 -*-

from .integration import Integration
import requests


class Hub(Integration):
    __properties__ = [
        'token', 'server'
    ]

    name = "hub"
    title = "HUB"
    description = "Private collaborative space"
    url = "http://workshopx.com"

    can_notify_group = False
    can_notify_users = False
    can_sync_users = True

    def fetch_users(self):

        # TODO
        url = "{base}/api/people".format(base=self.url)

        response = requests.get(url)
        if response.code != requests.OK:
            return []

        return []

    @classmethod
    def fields(self):
        return [
            dict(name="token", type="text", required=True),
            dict(
                name="server", type="url",
                placeholder="HUB base url", required=True
            )
        ]
