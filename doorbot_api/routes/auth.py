from flask import current_app, Blueprint, jsonify
auth = Blueprint('api', __name__, url_prefix='/api/auth')

from ..handlers import accounts

@auth.route('/password', methods=['POST'])
def password():
    accounts.register()
