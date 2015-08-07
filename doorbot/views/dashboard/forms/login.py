# -*- coding: utf-8 -*-

from wtforms import Form, PasswordField, StringField, validators


class PasswordLoginForm(Form):

    email = StringField('Email', [validators.Email])
    password = PasswordField('Password', [validators.Length(min=4)])


class ForgotPasswordForm(Form):
    email = StringField('Email', [validators.Email])
