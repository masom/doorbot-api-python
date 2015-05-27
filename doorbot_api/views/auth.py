from flask import current_app, Blueprint, jsonify
auth = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth.route('/password', methods=['POST'])
def password():
    pass
