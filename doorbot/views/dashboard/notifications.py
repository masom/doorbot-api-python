from flask import Blueprint
from ...container import container
from ...middlewares.dashboard import (render, s)

notifications = Blueprint(
    'notifications', __name__, url_prefix='/notifications'
)


def index():
    return dict(
        notifications=container.account.notifications.all()
    )


notifications.add_url_rule(
    '', 'index',
    s(index, render('notifications/index.html')),
    methods=['GET']
)
