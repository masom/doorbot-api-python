# -*- coding: utf-8 -*-


class IntegrationInterface(object):
    properties = []

    name = ""
    title = ""
    description = ""
    url = ""

    allow_multiple = False
    can_notify_users = False
    can_notify_group = False
    can_sync_users = False

    def __init__(self, integration_id, properties):
        self._properties = properties or {}
        self.integration_id = integration_id

    def get_service_user(self, notification):
        return notification.person.service_users.filter_by(
            service=self.name
        ).first()

    def fetch_users(self):
        raise NotImplementedError()

    def notify_user(self, notification):
        raise NotImplementedError()

    def notify_group(self, notification):
        raise NotImplementedError()

    @classmethod
    def fields(self):
        return []

    def __getattr__(self, attr):

        if attr in self.properties:
            return self._properties.get(attr, None)

        raise AttributeError(
            'Attribute `{attr}` does not exists'.format(attr=attr)
        )
