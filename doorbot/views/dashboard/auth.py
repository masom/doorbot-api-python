from flask import Blueprint, render_template, redirect, url_for
from .middlewares import m
from .forms.login import PasswordLoginForm
from ...container import container
from ...security import password_compare
from ...models import PersonAuthentication
from structlog import get_logger
logger = get_logger()


auth = Blueprint(
    'auth', __name__, url_prefix='/auth', template_folder='templates'
)


def login():
    form = PasswordLoginForm()
    return render_template('auth/password.html', form=form)


def password():
    form = PasswordLoginForm()
    if not form.validate:
        return render_template('auth/password.html', form=form)

    person = container.account.people.filter_by(email=form.email.data).first()
    if not person:
        return render_template('auth/password.html', form=form)

    authentication = person.authentications.filter_by(
        provider_id=PersonAuthentication.PROVIDER_PASSWORD
    ).first()

    if not authentication:
        logger.warning(
            'auth.password person has no password provider',
            account_id=person.account_id,
            person_id=person.id
        )
        return render_template('auth/password.html', form=form)

    if not password_compare(authentication.token, form.password):
        logger.info(
            'auth.password password does not match',
            account_id=person.account_id,
            person_id=person.id
        )
        return render_template('auth/password.html', form=form)

    return redirect(url_for('people.view', id=1))


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
    methods=['GET']
)

auth.add_url_rule(
    '/password', 'password',
    m(login),
    methods=['POST']
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
