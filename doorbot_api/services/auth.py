# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from ..auth import (PROVIDER_PASSWORD, PROVIDER_API_TOKEN)
from ..core import Repository
from ..security import generate_password


class Auth(Repository):
    def administrator_with_token(self, token):

        authrepo = self._repositories.authentication

        authentication = authrepo.find_by_provider_and_token(
            PROVIDER_API_TOKEN,
            token
        )

        if not authentication:
            logger.warning(
                '{module} administrator token not found'.format(
                    module=__name__
                ),
                token=token,
                module=__name__
            )

            return False

        administrator = self._repositories.administrators.find(
            authentication.administrator_id
        )

        if not administrator:
            logger.error(
                '{module} administrator not found'.format(
                    module=__name__
                ),
                account_id=self._repositories.account_id,
                token=token,
                administrator_id=authentication.administrator_id,
                module=__name__
            )

            return False

        return administrator

    def device_with_token(self, token):

        device = self._repositories.devices.find_by_token(token)

        if not device:
            logger.warning(
                '{module} device not found'.format(
                    module=__name__
                ),
                account_id=self._repositories.account_id,
                token=token,
                module=__name__
            )
            return False

        if not device.is_enabled:
            logger.info(
                '{module} device is disabled'.format(module=__name__),
                account_id=self._repositories.account_id,
                token=token,
                device_id=device.id,
                module=__name__
            )
            return False

        return device

    def person_with_token(self, token):

        parts = token.split(".")
        if len(parts) != 2:
            logger.warning(
                '{module} invalid person token'.format(module=__name__),
                account_id=self._repositories.account_id,
                token=token,
                module=__name__
            )

            return False

        try:
            id = int(parts[0], 10)
        except ValueError:
            logger.warning(
                '{module} invalid person id in token'.format(module=__name__),
                account_id=self._repositories.account_id,
                token=token,
                module=__name__
            )

            return False

        token = parts[1]

        authRepo = self._repositories.authentications
        auth = authRepo.find_by_provider_id_and_person_id_and_token(
            PROVIDER_API_TOKEN,
            id,
            token
        )

        if not auth:
            logger.info(
                '{module} authentication not found'.format(module=__name__),
                account_id=self._repositories.account_id,
                token=token,
                module=__name__
            )

            return False

        person = self._repositories.people.find(auth.person_id)

        if not person:
            logger.error(
                '{module} person not found'.format(module=__name__),
                account_id=self._repositories.account_id,
                token=token,
                person_id=auth.person_id,
                module=__name__
            )

            return False

        return person

    def person_with_password(self, email, password):
        person = self._repositories.people.first(email=email)
        authrepo = self._repositories.authentication

        if not person:
            logger.info(
                '{module} person not found'.format(module=__name__),
                account_id=self._repositories.account_id,
                email=email,
                module=__name__
            )

            return False

        authentication = authrepo.authentication.first(
            provider_id=PROVIDER_PASSWORD,
            person_id=person.id
        )

        if not authentication:
            logger.info(
                '{module} person has no password auth'.format(module=__name__),
                module=__name__,
                person_id=person.id,
                provider_id=PROVIDER_PASSWORD,
                account_id=self._repositories.account.id
            )

            return False

        token_auth = authrepo.authentication.first(
            provider_id=PROVIDER_API_TOKEN,
            person_id=person.id
        )

        if not token_auth:
            try:
                token_auth = authrepo.create(
                    person_id=person.id,
                    provider_id=PROVIDER_API_TOKEN,
                    token=generate_password(8)
                )
            except Exception as e:
                logger.error(
                    '{module} api token creation error'.format(
                        module=__name__
                    ),
                    module=__name__,
                    account_id=self._repositories.account_id,
                    person_id=person.id,
                    provider_id=PROVIDER_PASSWORD
                )

                raise e

        return dict(person=person, auth=token_auth)
