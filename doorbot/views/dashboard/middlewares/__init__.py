# -*- coding: utf-8 -*-
from flask import redirect, url_for
from ....middlewares import (account_scope, auth_secured, _logger_context)


def s(*mw):
    '''s defines a list of route middlewares that will be applied in order.
    '''

    return m(account_scope, auth_secured, *mw)


def m(*mw):
    '''m defines a list of route middlewares that will be applied in order.
    '''

    def wrapped(*args, **kwargs):
        _logger_context()
        for item in mw:
            rv = item(*args, **kwargs)
            if rv:
                if isinstance(rv, tuple):
                    if rv[1] == 401:
                        return redirect(url_for('auth.login'))
                return rv

    return wrapped
