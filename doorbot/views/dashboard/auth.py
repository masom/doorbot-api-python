from flask import Blueprint
from ...middlewares.dashboard import (m, render)

auth = Blueprint('auth', __name__, url_prefix='/auth')


def login():
    return dict()


def logout():
    return dict()


def reset_password(hash, nonce):
    return dict()


def forget_password():
    return dict()


def github():
    pass


def github_callback():
    pass


auth.add_url_rule(
    '/login', 'login',
    m(login, render('auth/login.html')),
    methods=['GET', 'POST']
)

auth.add_url_rule(
    '/logout', 'logout',
    m(logout),
    methods=['GET']
)

auth.add_url_rule(
    '/github', 'github',
    m(github),
    methods=['GET']
)

auth.add_url_rule(
    '/github/callback', 'github_callback',
    m(github_callback),
    methods=['GET']
)
