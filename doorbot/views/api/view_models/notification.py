# -*- coding: utf-8 -*-

from .model import ViewModel


class Notification(ViewModel):

    fields = []

    @classmethod
    def from_notification(cls, notification):
        return cls(
            created_at=notification.created_at,
            device_id=notification.device_id,
            door_id=notification.door_id,
            id=notification.id,
            person_id=notification.person_id,
        )
