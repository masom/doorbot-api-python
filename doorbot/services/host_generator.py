# -*- coding: utf-8 -*-

from ..core.service import Service
from ..security import generate_random_string


class HostGenerator(Service):
    '''Generates hosts'''

    def random(self, length):
        '''Generate a random hostname'''

        accounts = self._repositories.accounts

        for attempt in xrange(10):
            tmp = generate_random_string(length).lower()

            exists = accounts.first(dict(host=tmp))
            if exists:
                continue

            return tmp

        # TODO maybe throw an exception here?
        return None
