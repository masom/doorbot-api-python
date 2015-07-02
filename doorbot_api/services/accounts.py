# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

from ..core.service import Service
from ..security import generate_password, password_crypt


class Accounts(Service):

    def create(self, request):
        session = self._repositories.session

        try:
            host = self._generate_host(request.account.host)

            request.account.host = host
            account = self._create_account(request.account)

            self._repositories.set_account_scope(account.id)

            owner = self._create_account_owner(account, request.account)

            (auth, password) = self._create_account_owner_auth(owner)

            self._services.notifications.account_created(account, owner)

            session.commit()

            logger.info(
                '{module} account created'.format(module=__name__),
                module=__name__,
                account_id=account.id,
                account_host=account.host,
                person_id=auth.person_id,
                password=password
            )

        except Exception as e:
            logger.error(
                '{module} creation error'.format(module=__name__),
                error=e,
                module=__name__
            )

            session.rollback()

            return dict(account=None, error=e)

        return dict(account=account)

    def update(self, account, request):
        '''
        :param account:
        :param request:
        '''

        accounts = self._repositories.accounts

        account.name = request.account.name
        account.notifications_enabled = request.account.notifications_enabled
        account.notifications_email_enabled = request.account.notifications_email_enabled
        account.notifications_sms_enabled = request.account.notifications_sms_enabled

        accounts.save(account, True)

    def delete(self, account):
        accounts = self._repositories.accounts

        accounts.delete(account)

        logger.info(
            '{module} account deleted'.format(module=__name__),
            module=__name__,
            account_id=account.id
        )

    def _generate_host(self, requested):
        accounts = self._repositories.accounts

        if requested:
            exists = accounts.first(dict(host=requested))

            if exists:
                logger.warning(
                    '{module} host is already taken'.format(module=__name__),
                    module=__name__,
                    host=requested
                )

                return False

            host = requested
        else:
            host = self._services.host_generator.random(10)

        if not host:
            logger.error(
                '{module} invalid host'.format(module=__name__),
                requested=requested,
                host=host,
                module=__name__
            )

            return False

        return host

    def _create_account(self, requested):
        '''
        :param request:
        '''

        accounts = self._repositories.accounts

        account = accounts.new()
        account.host = requested.host
        account.name = requested.name
        account.contact_name = requested.contact_name
        account.contact_email = requested.contact_email
        account.contact_phone_number = requested.contact_phone_number

        account.is_enabled = False
        account.notifications_enabled = False
        account.notifications_sms_enabled = False
        account.notifications_email_enabled = False

        accounts.save(account, False)

        return account

    def _create_account_owner(self, account, requested):
        '''
        :param account:
        :param requested:
        '''

        people = self._repositories.people

        person = people.new()
        person.name = requested.contact_name
        person.email = requested.contact_email
        person.account_type = account.TYPE_OWNER

        people.create(person, False)

        return person

    def _create_account_owner_auth(self, owner):
        '''
        :param owner:
        '''

        authentications = self._repositories.authentications

        password = generate_password(8)

        auth = authentications.new()
        auth.person_id = owner.id
        auth.provider_id = auth.PROVIDER_PASSWORD
        auth.token = password_crypt(password)

        authentications.save(auth, False)

        return (auth, password)
