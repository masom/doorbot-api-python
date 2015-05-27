# -*- coding: utf-8 -*-


from flask import current_app, Blueprint, jsonify, g, request
accounts = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@accounts.route('', methods=['GET'])
def index():
    repositories = current_app.doorbot_repositories

    return jsonify(dict(accounts=repositories.accounts.all()))


@accounts.route('/register', methods=['POST'])
def register():

    services = current_app.doorbot_services
    services.accounts.register(data)
