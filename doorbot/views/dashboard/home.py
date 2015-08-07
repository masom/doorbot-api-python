# -*- coding: utf-8 -*-
from flask import Blueprint, render_template
from .middlewares import s


home = Blueprint('home', __name__)


def dashboard():
    return render_template('home/home.html')


home.add_url_rule(
    '/', 'dashboard', s(home), methods=['GET']
)
