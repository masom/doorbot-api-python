# -*- coding: utf-8 -*-

from .model import ViewModel


class Integration(ViewModel):

    fields = ['created_at', 'name', 'updated_at']

    @classmethod
    def from_integration(cls, integration):
        return cls(
            created_at=integration.created_at,
            name=integration.name,
            updated_at=integration.updated_at
        )
