# -*- coding: utf-8 -*-

from werkzeug.serving import run_simple
from doorbot.factory import SubdomainDispatcher
import logging
logging.basicConfig()

import structlog

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
    config=None,
    debug=True
)

run_simple('localhost', 5000, application,
           use_reloader=True, use_debugger=True, use_evalex=True)
