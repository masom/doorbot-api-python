# -*- coding: utf-8 -*-

from .hipchat import HipChat
from .hub import Hub
from .mailgun import Mailgun
from .nexmo import Nexmo
from .postmark import Postmark
from .slack import Slack
from .twilio import Twilio
from .webhook import Webhook

available_integrations = [
    HipChat,
    Hub,
    Mailgun,
    Nexmo,
    Postmark,
    Slack,
    Twilio,
    Webhook
]
