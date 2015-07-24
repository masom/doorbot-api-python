# -*- coding: utf-8 -*-

from .integration import IntegrationInterface
# import requests


class Hub(IntegrationInterface):
    properties = [
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

        """
        url = "{base}/api/people".format(base=self.url)

        response = requests.get(url)
        if response.code != request.OK:
            return []
        """
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
