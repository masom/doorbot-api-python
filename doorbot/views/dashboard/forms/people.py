# -*- coding: utf-8 -*-

from wtforms import BooleanField, Form, StringField, validators
from wtforms.fields.html5 import EmailField


class CreatePersonForm(Form):

    name = StringField('Name', [validators.Length(min=2, max=50)])
    email = EmailField('Email', [validators.Email])


class UpdatePersonForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=50)])
    email = EmailField('Email', [validators.Email])

    is_available = BooleanField('Available')
    is_visible = BooleanField('Visible')
