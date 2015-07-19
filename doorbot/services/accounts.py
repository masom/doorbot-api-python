# -*- coding: utf-8 -*-


from ..core.service import Service
from ..security import generate_password, password_crypt
from structlog import get_logger

logger = get_logger()


class Accounts(Service):

    def create(self, data):
        session = self._repositories.session

        try:
            host = self._generate_host(data['host'])

            data.host = host

            account = self._create_account(data)

            self._repositories.set_account_scope(account.id)

            owner = self._create_account_owner(account, data)

            (auth, password) = self._create_account_owner_auth(owner)

            self._services.notifications.account_created(account, owner)

            session.commit()

            logger.info(
                'account created', dict(
                    account_id=account.id,
                    account_host=account.host,
                    person_id=auth.person_id,
                    password=password
                )
            )

        except Exception as e:
            logger.error(
                'account creation error',
                error=e
            )

            session.rollback()

            return dict(account=None, error=e)

        return dict(account=account)

    def update(self, account, data):
        '''
        :param account:
        :param data:
        '''

        accounts = self._repositories.accounts

        account.name = data.account.name
        account.notifications_enabled = data.account.notifications_enabled
        account.notifications_email_enabled = data.account.notifications_email_enabled
        account.notifications_sms_enabled = data.account.notifications_sms_enabled

        accounts.save(account, True)

    def delete(self, account):
        accounts = self._repositories.accounts

        accounts.delete(account)

        logger.info(
            '{module} account deleted',
            extra=dict(
                module=__name__,
                account_id=account.id
            )
        )

    def _generate_host(self, data):
        accounts = self._repositories.accounts

        if data:
            exists = accounts.first(host=data)

            if exists:
                logger.warning(
                    'account register host is already taken',
                    host=data
                )

                return False

            host = data
        else:
            host = self._services.host_generator.random(10)

        if not host:
            logger.error(
                'account register invalid host',
                data=data
            )

            return False

        logger.info('account host generated', host=host)
        return host

    def _create_account(self, data):
        '''
        :param data:
        '''

        accounts = self._repositories.accounts

        account = accounts.new()
        account.host = data.host
        account.name = data.name
        account.contact_name = data.contact_name
        account.contact_email = data.contact_email
        account.contact_phone_number = data.contact_phone_number

        account.is_enabled = False
        account.notifications_enabled = False
        account.notifications_sms_enabled = False
        account.notifications_email_enabled = False

        accounts.save(account, False)

        return account

    def _create_account_owner(self, account, data):
        '''
        :param account:
        :param data:
        '''

        people = self._repositories.people

        person = people.new()
        person.name = data.contact_name
        person.email = data.contact_email
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
