# -*- coding: utf-8 -*-

AUTHORIZATION_GATEKEEPER = 'gatekeeper'
AUTHORIZATION_PERSON = 'person'
AUTHORIZATION_DEVICE = 'device'
AUTHORIZATION_ADMINISTRATOR = 'administrator'


def administrator_with_token(repositories, token):

    authentication = repositories.authentications.find_by_provider_and_token(
        PROVIDER_API_TOKEN,
        token
    )

    if not authentication:

        # TODO log
        return False

    administrator = repositories.administrators.find(
        authentication.administrator_id
    )

    if not administrator:
        # TODO log
        return False

    return administrator


def device_with_token(repositories, token):

    device = repositories.devices.find_by_token(token)

    if not device:
        # TODO log
        return False

    if not device.is_enabled:
        # TODO log
        return False

    return device


def person_with_token(repositories, token):

    parts = token.split(".")
    if len(parts) != 2:
        # TODO log
        return False

    id = int(parts[0], 10)
    token = parts[1]


    authRepo = repositories.authentications
    auth = authRepo.find_by_provider_id_and_person_id_and_token(
        PROVIDER_API_TOKEN,
        id,
        token
    )

    if not auth:
        # TODO log
        return False

    person = repositories.people.find(auth.person_id)

    if not person:
        # TODO log
        return False

    return person
