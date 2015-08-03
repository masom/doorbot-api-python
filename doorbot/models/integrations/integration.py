# -*- coding: utf-8 -*-


class IntegrationInterface(object):
    properties = []

    name = ""
    title = ""
    description = ""
    url = ""

    allow_multiple = False
    can_notify_people = False
    can_notify_group = False
    can_sync_people = False

    def __init__(self, integration):
        self._properties = integration.properties or {}
        self.integration = integration

    def get_service_user(self, notification):
        return notification.person.service_users.filter_by(
            service=self.name
        ).first()

    def fetch_people(self):
        raise NotImplementedError()

    def notify_person(self, notification, delivery):
        raise NotImplementedError()

    def notify_group(self, notification, delivery):
        raise NotImplementedError()

    @classmethod
    def fields(self):
        return []

    def __getattr__(self, attr):
        if attr in self.properties:
            return self._properties.get(attr, None)
