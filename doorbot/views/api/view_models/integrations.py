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
            name=integration.name,
            updated_at=integration.updated_at
        )

        for key in integration.__properties__:
            setattr(instance, key, getattr(integration, key))

        return instance
