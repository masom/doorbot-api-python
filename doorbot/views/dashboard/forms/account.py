# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators


class UpdateAccountForm(Form):
    name = StringField('name', [validators.Length(min=3)])
