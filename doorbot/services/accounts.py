# -*- coding: utf-8 -*-


from ..core.service import Service
from ..security import generate_password, password_crypt
from ..auth import PROVIDER_PASSWORD
from structlog import get_logger
from ..models import Account, Person, PersonAuthentication


logger = get_logger()


class AccountCreatedResult(object):
    def __init__(self, account, error):
        self.account = account
        self.error = error


class Accounts(Service):

    def create(self, data):
        database = self.database

        try:
            host = self._generate_host(data['host'])

            data['host'] = host

            account = self._create_account(data)

            owner = self._create_account_owner(account, data)

            (auth, password) = self._create_account_owner_auth(owner)

            self.services.notifications.account_created(account, owner)

            database.commit()

            logger.info(
                'account created',
                account_id=account.id,
                account_host=account.host,
                person_id=auth.person_id,
                password=password
            )

        except Exception as e:
            import traceback

            logger.error(
                'account creation error',
                error=e,
                trace=traceback.format_exc()
            )

            database.rollback()

            return AccountCreatedResult(account=None, error=e)

        return AccountCreatedResult(account=account)

    def update(self, account, data):
        '''
        :param account:
        :param data:
        '''

        account.name = data.account.name
        account.notifications_enabled = data.account.notifications_enabled
        account.notifications_email_enabled = \
            data.account.notifications_email_enabled
        account.notifications_sms_enabled = \
            data.account.notifications_sms_enabled

    def delete(self, account):
        self.database.delete(account)

        logger.info(
            '{module} account deleted',
            extra=dict(
                module=__name__,
                account_id=account.id
            )
        )

    def _generate_host(self, data):
        if data:
            exists = self.database.query(Account).filter_by(host=data).first()

            if exists:
                logger.warning(
                    'account register host is already taken',
                    host=data
                )

                return False

            host = data
        else:
            host = self.services.host_generator.random(10)

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

        account = Account()
        account.host = data['host']
        account.name = data['name']
        account.contact_name = data['contact_name']
        account.contact_email = data['contact_email']
        account.contact_phone_number = data['contact_phone_number']

        account.is_enabled = True
        account.notifications_enabled = False
        account.notifications_sms_enabled = False
        account.notifications_email_enabled = False

        self.database.add(account)

        return account

    def _create_account_owner(self, account, data):
        '''
        :param account:
        :param data:
        '''

        person = Person()
        person.name = data['contact_name']
        person.email = data['contact_email']
        person.account_type = account.TYPE_OWNER

        account.people.append(person)

        return person

    def _create_account_owner_auth(self, owner):
        '''
        :param owner:
        '''

        password = generate_password(8)

        authentication = PersonAuthentication()
        authentication.person_id = owner.id
        authentication.provider_id = PROVIDER_PASSWORD
        authentication.token = password_crypt(password)

        owner.authentications.append(authentication)

        return (authentication, password)
