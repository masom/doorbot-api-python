# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from doorbot_api.factory import SubdomainDispatcher


application = SubdomainDispatcher(
    domain='doorbot.dev',
    config=None,
    debug=True
)

run_simple('localhost', 5000, application,
           use_reloader=True, use_debugger=True, use_evalex=True)
