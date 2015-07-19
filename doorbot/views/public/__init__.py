from flask import Blueprint, jsonify, request, render_template, redirect
from ...container import container
from .forms import RegistrationForm

public = Blueprint(
    'public', __name__, url_prefix='/', template_folder='templates'
)


@public.route('', methods=['GET'])
def home():
    return 'Welcome to Doorbot'


@public.route('/status')
def status():
    return jsonify(dict(status="ok"))


@public.route('register', methods=['GET'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)


@public.route('register', methods=['POST'])
def do_register():

    form = RegistrationForm(request.form)

    if not form.validate():
        return render_template('register.html', form=form)

    services = container.services
    result = services.accounts.create(request.data)

    if result.get('error', False):
        return dict(result.error), 500

    return redirect("{host}.doorbot.dev".format(host=result.account.host))
