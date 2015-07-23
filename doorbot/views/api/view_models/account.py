# -*- coding: utf-8 -*-

from .model import ViewModel


class Account(ViewModel):
    fields = [
        'id', 'name', 'host', 'contact_name', 'contact_email',
        'contact_phone_number'
    ]

    @classmethod
    def from_account(cls, account):
        return cls(
            id=account.id,
            name=account.name,
            host=account.host,
            contact_name=account.contact_name,
            contact_email=account.contact_email,
            contact_phone_number=account.contact_phone_number
        )


class PublicAccount(ViewModel):

    fields = ['id', 'name', 'host']

    @classmethod
    def from_account(cls, account):
        return cls(
            id=account.id,
            name=account.name,
            host=account.host
        )
