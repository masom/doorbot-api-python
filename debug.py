# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from doorbot.factory import (
    SubdomainDispatcher,
    create_api_app, create_admin_app, create_dashboard_app, create_public_app
)
import logging
import structlog
import sys


root = logging.getLogger('doorbot')
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
root.addHandler(ch)
root.propagate = False


structlog.configure(
    processors=[
        structlog.processors.KeyValueRenderer(
            key_order=['request_id'],
        ),
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
)

application = SubdomainDispatcher(
    domain='doorbot.dev',
    config='../config.py',
    debug=True
)

application.add_app_factory('admin', create_admin_app)
application.add_app_factory('api', create_api_app)
application.add_app_factory('dashboard', create_dashboard_app)
application.add_app_factory('public', create_public_app)
application.initialize()

run_simple('localhost', 5000, application,
           use_reloader=True, use_debugger=True, use_evalex=True)
