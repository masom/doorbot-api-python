# -*- coding: utf-8 -*-

from .model import ViewModel


class Integration(ViewModel):

    fields = [
        'created_at', 'description', 'name', 'title', 'updated_at'
    ]

    @classmethod
    def from_integration(cls, integration):
        instance = cls(
            created_at=integration.created_at,
            name=integration.adapter.name,
            description=integration.adapter.description,
            updated_at=integration.updated_at
        )

        for key in integration.adapter.properties:
            if hasattr(integration, key):
                value = getattr(integration, key)
            else:
                value = None

            setattr(instance, key, value)

        return instance
