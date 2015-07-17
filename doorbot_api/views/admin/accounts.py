from flask import Blueprint, jsonify, request
from ...container import container
from ...middleswares import (
    m, auth_admin, auth_secured
)

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')


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


def index():
    repositories = container.repositories

    accounts = [
        PublicAccount.from_account(account).to_dict()
        for account in repositories.accounts.all()
    ]

    return jsonify(dict(
        accounts=accounts
    ))


def create():

    services = container.services
    result = services.accounts.register(request.data)

    if result.get('error', False):
        return jsonify(dict()), 500

    return jsonify(dict(
        account=result.get('account', None)
    ))


def update(id):

    account = container.repositories.accounts.first(id=id)

    if not account:
        pass

    container.services.accounts.update(account)

    return jsonify(dict(
        account=account
    ))

accounts.add_url_rule(
    '', 'index', m(auth_secured, auth_admin, index),
    methods=['GET']
)

accounts.add_url_rule(
    '', 'create', m(auth_secured, auth_admin, create),
    methods=['POST']
)

accounts.add_url_rule(
    '/<int:id>', 'update', m(auth_secured, auth_admin, update),
    methods=['PUT']
)
