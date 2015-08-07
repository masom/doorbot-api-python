# -*- coding: utf-8 -*-

from .account import account
from .account_transactions import account_transactions
from .auth import auth
from .devices import devices
from .doors import doors
from .home import home
from .integrations import integrations
from .notifications import notifications
from .people import people
from .people_authentications import people_authentications


blueprints = [
    account,
    account_transactions,
    auth,
    devices,
    doors,
    home,
    integrations,
    notifications,
    people,
    people_authentications
]
