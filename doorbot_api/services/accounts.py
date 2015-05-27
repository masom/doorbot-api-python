# -*- coding: utf-8 -*-

from ..core.service import Service
from ..security import generate_password, password_crypt


class Accounts(Service):

    def register(self, request):
        try:
            host = self._generate_host(request.account.host)

            request.account.host = host
            account = self._create_account(request.account)

            self._repositories.set_account_scope(account.id)

            owner = self._create_account_owner(account, request.account)

            (auth, password) = self._create_account_owner_auth(owner)

            self._services.notifications.account_created(account, owner)

            self._repositories.database_session().commit()
        except Exception as e:
            self._repositories.database_ession().rollback()
            raise e

        return dict(account=account, owner=owner, password=password)

    def update(self, account, request):
        accounts = self._repositories.accounts

        account.name = request.account.name
        account.notifications_enabled = request.account.notifications_enabled
        account.notifications_email_enabled = request.account.notifications_email_enabled
        account.notifications_sms_enabled = request.account.notifications_sms_enabled

        accounts.update(account, True)

    def delete(self, account):
        accounts = self._repositories.accounts

        accounts.delete(account)

    def _generate_host(self, requested):
        accounts = self._repositories.accounts

        if requested:
            exists = accounts.first(dict(host=requested))

            if exists:
                # TODO response object with resolution
                return False

            host = requested
        else:
            host = self._services.host_generator.random(10)

        if not host:
            # TODO Service Unavailable
            return False

        return host

    def _create_account(self, requested):
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
        people = self._repositories.people

        person = people.new()
        person.name = requested.contact_name
        person.email = requested.contact_email
        person.account_type = account.TYPE_OWNER

        people.create(person, False)

        return person


    def _create_account_owner_auth(self, owner):
        authentications = self._repositories.authentications

        password = generate_password(8)

        auth = authentications.new()
        auth.person_id = person.id
        auth.provider_id = authentication.PROVIDER_PASSWORD
        auth.token = password_crypt(password)

        authentications.save(auth, False)

        return (auth, password)
