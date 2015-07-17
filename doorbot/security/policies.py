# -*- coding: utf-8 -*-

from .roles import (ACCOUNT_OWNER, ACCOUNT_MEMBER, ACCOUNT_MANAGER)

policy = dict(
    account_delete=False,
    account_update=False,
    account_list=False,
    account_view=False,

    device_create=False,
    device_delete=False,
    device_update=False,
    device_list=False,
    device_view=False,

    door_create=False,
    door_delete=False,
    door_update=False,
    door_list=False,
    door_view=False,

    person_create=False,
    person_delete=False,
    person_update=False,
    person_list=False,
    person_view=False,
)


class Policy:
    def __init__(self):
        for item, value in policy.iteritems():
            setattr(self, item, value)

    def can_update_person(self, a_id, b_id):
        return self.person_update or a_id == b_id


class AccountOwnerPolicy(Policy):
    def __init__(self):
        for item in policy.iterkeys():
            setattr(self, item, True)


class AdministratorPolicy(Policy):
    def __init__(self):
        for item in policy.iterkeys():
            setattr(self, item, True)


class DevicePolicy(Policy):
    def __init__(self):
        super().__init__()

        self.door_list = True
        self.door_view = True
        self.person_list = True


class ManagerPolicy(Policy):

    def __init__(self):
        for item in policy.iterkeys():
            setattr(self, item, True)

        self.account_delete = False


class MemberPolicy(Policy):
    def __init__(self):
        super().__init__()

        self.account_view = True
        self.door_list = True
        self.door_view = True
        self.person_list = True
        self.person_view = True

policies = dict(
    ACCOUNT_OWNER=AccountOwnerPolicy,
    ACCOUNT_MEMBER=MemberPolicy,
    ACCOUNT_MANAGER=ManagerPolicy
)


def get_policy_for_person(person):
    policy = policies.get(person.account_type, None)

    if policy:
        return policy()
    return None
