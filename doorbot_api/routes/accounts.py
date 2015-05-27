# -*- coding: utf-8 -*-


from flask import current_app, Blueprint, jsonify, g, request
accounts = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@accounts.route('/', methods=['GET'])
def index():
    repositories = g.get('doorbot-repositories')

    return jsonify(dict(accounts=repositories.accounts.all()))


@accounts.route('/register', methods=['POST'])
def register():
    services = g.get('doorbot-services')

    services.accounts.register(data)
