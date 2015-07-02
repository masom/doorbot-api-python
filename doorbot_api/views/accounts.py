# -*- coding: utf-8 -*-


from flask import Blueprint, jsonify, request
from ..container import container

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


@accounts.route('', methods=['GET'])
def index():
    repositories = container.repositories

    accounts = [
        PublicAccount.from_account(account).to_dict()
        for account in repositories.accounts.all()
    ]

    return jsonify(dict(
        accounts=accounts
    ))


@accounts.route('/register', methods=['POST'])
def create():

    services = container.services
    result = services.accounts.register(request.data)

    if result.get('error', False):
        pass

    return jsonify(dict(
        account=result.get('account', None)
    ))


@accounts.route('/<int:id>', methods=['GET'])
def get(id):
    repositories = container.repositories

    return jsonify(dict(
        account=repositories.accounts.first(id=id)
    ))


@accounts.route('/<int:id>', methods=['PUT'])
def update(id):

    account = container.repositories.accounts.first(id=id)

    if not account:
        pass

    container.services.accounts.update(account)

    return jsonify(dict(
        account=account
    ))


@accounts.route('/<int:id>', methods=['DELETE'])
def delete():
    pass
