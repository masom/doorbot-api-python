# -*- coding: utf-8 -*-
from ..auth import (PROVIDER_PASSWORD, PROVIDER_API_TOKEN)
from ..core.service import Service
from ..security import generate_api_token
from structlog import get_logger
from ..models import (
    Administrator, AdministratorAuthentication, PersonAuthentication
)

logger = get_logger()


class Auth(Service):
    def administrator_with_token(self, token):

        db = self.database
        auth = db.query(AdministratorAuthentication).filter_by(
            provider_id=PROVIDER_API_TOKEN,
            token=token
        ).first()

        if not auth:
            logger.warning(
                '{module} administrator token not found'.format(
                    module=__name__
                ),
                token=token,
                module=__name__
            )

            return False

        administrator = db.query(Administrator).filter_by(
            id=auth.administrator_id
        ).first()

        if not administrator:
            logger.error(
                '{module} administrator not found'.format(
                    module=__name__
                ),
                account_id=self.account.id,
                token=token,
                administrator_id=auth.administrator_id,
                module=__name__
            )

            return False

        return administrator

    def device_with_token(self, token):

        device = self.account.devices.filter_by(token=token).first()

        if not device:
            logger.warning(
                '{module} device not found'.format(
                    module=__name__
                ),
                account_id=self.account.id,
                token=token,
                module=__name__
            )
            return False

        if not device.is_enabled:
            logger.info(
                '{module} device is disabled'.format(module=__name__),
                account_id=self.account_id,
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
                account_id=self.account.id,
                token=token,
                module=__name__
            )

            return False

        try:
            person_id = int(parts[0], 10)
        except ValueError:
            logger.warning(
                '{module} invalid person id in token'.format(module=__name__),
                account_id=self.account.id,
                token=token,
                module=__name__
            )

            return False

        token = parts[1]

        auth = self.database.query(PersonAuthentication).filter_by(
            account_id=self.account.id,
            provider_id=PROVIDER_API_TOKEN,
            person_id=person_id,
            token=token
        ).first()

        if not auth:
            logger.info(
                '{module} authentication not found'.format(module=__name__),
                account_id=self.account.id,
                token=token,
                module=__name__
            )

            return False

        return auth.person

    def person_with_password(self, email, password):
        person = self.account.people.filter_by(email=email).first()

        if not person:
            return False

        auth = person.authentications.filter_by(
            provider_id=PROVIDER_PASSWORD
        ).first

        if not auth:
            logger.info(
                '{module} person has no password auth'.format(module=__name__),
                module=__name__,
                person_id=person.id,
                provider_id=PROVIDER_PASSWORD,
                account_id=self.account.id
            )

            return False

        token_auth = person.authentications.filter_by(
            provider_id=PROVIDER_API_TOKEN,
            person_id=person.id
        ).first()

        if not token_auth:
            try:
                token_auth = PersonAuthentication()
                token_auth.provider_id = PROVIDER_API_TOKEN
                token_auth.token = generate_api_token()

                person.authentications.append(token_auth)

                self.database.commit()
            except Exception as e:
                logger.error(
                    '{module} api token creation error'.format(
                        module=__name__
                    ),
                    module=__name__,
                    account_id=self.account.id,
                    person_id=person.id,
                    provider_id=PROVIDER_PASSWORD
                )

                raise e

        return dict(person=person, auth=token_auth)
