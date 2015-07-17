from flask import Blueprint, jsonify, request
from ...container import container

public = Blueprint('public', __name__, url_prefix='')


@public.route('', methods=['GET'])
def home():
    return 'Welcome to Doorbot'


@public.route('/status')
def status():
    return jsonify(dict(status="ok"))


@public.route('/register', methods=['GET'])
def register():
    return 'derp'


@public.route('/register', methods=['POST'])
def do_register():

    services = container.services
    result = services.accounts.register(request.data)

    if result.get('error', False):
        return jsonify(dict()), 500

    return jsonify(dict(
        account=result.get('account', None)
    ))
