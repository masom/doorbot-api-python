from flask import Blueprint

people = Blueprint('people', __name__, url_prefix='/people')


@people.route('/sync', methods=['POST'])
def sync():
    pass
