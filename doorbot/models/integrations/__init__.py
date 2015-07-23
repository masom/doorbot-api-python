# -*- coding: utf-8 -*-

from .hipchat import HipChat
from .hub import Hub
from .mailgun import Mailgun
from .nexmo import Nexmo
from .postmark import Postmark
from .slack import Slack
from .twilio import Twilio

available_integrations = [
    HipChat,
    Hub,
    Mailgun,
    Nexmo,
    Postmark,
    Slack,
    Twilio
]


def polymorph_integration(integration):

    for cls in available_integrations:
        if integration.name == cls.name:
            return cls.polymorph(integration)

    raise RuntimeError(
        "Integration {name} is not available".format(name=integration.name)
    )
