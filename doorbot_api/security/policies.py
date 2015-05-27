# -*- coding: utf-8 -*-

policy = dict(
    account_delete=false,
    account_update=false,
    account_list=false,
    account_view=false,

    device_create=false,
    device_delete=false,
    device_update=false,
    device_list=false,
    device_view=false,

    door_create=false,
    door_delete=false,
    door_update=false,
    door_list=false,
    door_view=false,

    person_create=false,
    person_delete=false,
    person_update=false,
    person_list=false,
    person_view=false,
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
