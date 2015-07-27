# -*- coding: utf-8 -*-

from .model import ViewModel


class Door(ViewModel):

    fields = ['created_at', 'id', 'name']

    @classmethod
    def from_door(cls, door):
        return cls(
            created_at=door.created_at,
            id=door.id,
            name=door.name
        )


class PublicDoor(ViewModel):

    fields = ['id', 'name']

    @classmethod
    def from_door(cls, door):
        return cls(
            id=door.id,
            name=door.name
        )
