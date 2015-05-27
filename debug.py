# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from doorbot_api.factory import create_app

app = create_app()
app.debug = True

run_simple('localhost', 5000, app,
           use_reloader=True, use_debugger=True, use_evalex=True)
