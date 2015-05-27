# -*- coding: utf-8 -*-


from flask import Blueprint, jsonify, request
from ..container import container

accounts = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@accounts.route('', methods=['GET'])
def index():
    repositories = container.repositories

    return jsonify(dict(accounts=repositories.accounts.all()))


@accounts.route('/register', methods=['POST'])
def register():

    services = container.services
    services.accounts.register(request.data)
