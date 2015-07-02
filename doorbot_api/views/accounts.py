# -*- coding: utf-8 -*-


from flask import Blueprint, jsonify, request
from ..container import container

accounts = Blueprint('accounts', __name__, url_prefix='/accounts')


@accounts.route('', methods=['GET'])
def index():
    repositories = container.repositories

    return jsonify(dict(
        accounts=repositories.accounts.all()
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
def update():
    pass


@accounts.route('/<int:id>', methods=['DELETE'])
def delete():
    pass
