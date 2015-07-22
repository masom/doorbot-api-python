# -*- coding: utf-8 -*-

from ..core.service import Service
from ..security import generate_random_string
from ..models import Account


class HostGenerator(Service):
    '''Generates hosts'''

    def random(self, length):
        '''Generate a random hostname'''

        for attempt in xrange(10):
            tmp = generate_random_string(length).lower()

            exists = self.database.query(Account).filter_by(host=tmp).first()
            if exists:
                continue

            return tmp

        # TODO maybe throw an exception here?
        return None
