# -*- coding: utf-8 -*-

import logging
from .security.policies import (
    AdministratorPolicy, get_policy_for_person
)

logger = logging.getLogger(__name__)

AUTHORIZATION_GATEKEEPER = 'gatekeeper'
AUTHORIZATION_PERSON = 'person'
AUTHORIZATION_DEVICE = 'device'
AUTHORIZATION_ADMINISTRATOR = 'administrator'

PROVIDER_API_TOKEN = 2
PROVIDER_PASSWORD = 1


class Authorization(object):
    def __init__(self):
        self.type = None
        self.administrator = None
        self.person = None
        self.device = None
        self.policy = None

    def update_to_administrator(self, administrator):
        self.clear()

        self.type = AUTHORIZATION_ADMINISTRATOR
        self.administrator = administrator
        self.policy = AdministratorPolicy()

    def update_to_person(self, person):
        self.clear()

        self.type = AUTHORIZATION_PERSON
        self.person = person
        self.policy = get_policy_for_person(person)

    def clear(self):
        self.type = None
        self.administrator = None
        self.device = None
        self.person = None
        self.policy = None


def parse_token_authorization(authorization):

    if not authorization:
        logger.info(
            '{method} missing authorization header',
            module=__name__,
            method='parse_token_authorization'
        )
        return False, False

    parts = authorization.split(' ')
    if len(parts) != 2:
        logger.info(
            '{method} invalid authorization header',
            module=__name__,
            method='parse_token_authorization'
        )
        return False, False

    return parts[0], parts[1]
