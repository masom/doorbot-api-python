# -*- coding: utf-8 -*-


from flask import Blueprint, jsonify
from ...container import container
from ...middleswares import (
    m, auth_owner, auth_secured
)

accounts = Blueprint('account', __name__, url_prefix='/account')


class PublicAccount(object):

    def __init__(self, id, name, host):
        self.name = name
        self.id = id
        self.host = host

    def to_dict(self):
        return dict(id=self.id, name=self.name, host=self.host)

    @classmethod
    def from_account(cls, account):
        return cls(
            id=account.id,
            name=account.name,
            host=account.host
        )


def view():
    account = container.account
    authorization = container.authorization

    if authorization.is_administrator():
        return jsonify(dict(
            account=account
        ))

    if authorization.is_person():
        if authorization.person.is_account_manager():
            return jsonify(dict(
                account=account
            ))
        else:
            return jsonify(dict(
                account=PublicAccount.from_account(account).to_dict()
            ))

    return jsonify(dict()), 403


def update():

    account = container.repositories.accounts.first(id=id)

    if not account:
        pass

    container.services.accounts.update(account)

    return jsonify(dict(
        account=account
    ))

accounts.add_url_rule(
    '', 'view', m(auth_secured, view),
    methods=['GET']
)

accounts.add_url_rule(
    '', 'update', m(auth_secured, auth_owner, update),
    methods=['PUT']
)
