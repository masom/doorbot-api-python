# -*- coding: utf-8 -*-

from .model import ViewModel


class Device(ViewModel):

    fields = [
        'created_at', 'description', 'device_id', 'door_id', 'id',
        'is_enabled', 'name', 'token', 'updated_at'
    ]

    @classmethod
    def from_device(cls, device):
        return cls(
            id=device.id,
            name=device.name,
            token=device.token,
            created_at=device.created_at,
            updated_at=device.updated_at
        )


class PublicDevice(ViewModel):
    fields = ['description', 'door_id', 'id', 'is_enabled', 'name']

    @classmethod
    def from_device(cls, device):
        return cls(
            description=device.description,
            id=device.id,
            door_id=device.door_id,
            is_enabled=device.is_enabled,
            name=device.name
        )
