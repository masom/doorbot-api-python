from flask import Blueprint
from ...middlewares import (
    m, auth_secured, auth_manager
)


people = Blueprint('people', __name__, url_prefix='/people')


@people.route('/sync', methods=['POST'])
def sync():
    pass


people.add_url_rule(
    '/sync', 'sync', m(auth_secured, auth_manager, sync), methods=['POST']
)
