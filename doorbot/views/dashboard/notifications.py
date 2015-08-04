from flask import Blueprint, render_template
from ...container import container
from .middlewares import s

notifications = Blueprint(
    'notifications', __name__, url_prefix='/notifications'
)


def index():
    return render_template(
        'notifications/index.html',
        notifications=container.account.notifications.all()
    )


notifications.add_url_rule(
    '', 'index',
    s(index),
    methods=['GET']
)
