from flask import current_app, Blueprint, jsonify
routes = Blueprint('api', __name__, url_prefix='/api')

@routes.route('/status')
def status():
    return jsonify(dict(status="ok"))
