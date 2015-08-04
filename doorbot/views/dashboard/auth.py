from flask import Blueprint, render_template, redirect, url_for
from .middlewares import m

auth = Blueprint('auth', __name__, url_prefix='/auth')


def login():
    return render_template('auth/login.html')


def logout():
    return redirect(url_for('.login'))


def reset_password(hash, nonce):
    return render_template('auth/reset_password.html')


def forgot_password():
    return render_template('auth/forgot_password.html')


def github():
    github_redirect_url = ''
    return redirect(github_redirect_url)


def github_callback():
    pass


auth.add_url_rule(
    '/login', 'login',
    m(login),
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
