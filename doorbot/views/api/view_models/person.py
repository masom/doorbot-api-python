# -*- coding: utf-8 -*-

from .model import ViewModel


class Person(ViewModel):

    fields = [
        'created_at', 'email', 'id', 'is_visible', 'is_available',
        'name', 'notifications_enabled', 'notifications_app_enabled',
        'notifications_chat_enabled', 'notifications_email_enabled',
        'notifications_sms_enabled',
        'phone_number', 'title', 'updated_at'
    ]

    @classmethod
    def from_person(cls, person):
        return cls(
            created_at=person.created_at,
            email=person.email,
            id=person.id,
            is_visible=person.is_visible,
            is_available=person.is_available,
            name=person.name,
            notifications_enabled=person.notifications_enabled,
            notifications_app_enabled=person.notifications_app_enabled,
            notifications_chat_enabled=person.notifications_chat_enabled,
            notifications_email_enabled=person.notifications_email_enabled,
            notifications_sms_enabled=person.notifications_sms_enabled,
            title=person.title,
            updated_at=person.updated_at,
        )


class PublicPerson(ViewModel):

    fields = ['id', 'email', 'is_visible', 'is_available', 'name', 'title']

    @classmethod
    def from_person(cls, person):
        return cls(
            id=person.id,
            email=person.email,
            is_visible=person.is_visible,
            is_available=person.is_available,
            name=person.name,
            title=person.title
        )
