# -*- coding: utf-8 -*-
import datetime


class ViewModel(object):

    fields = []

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.fields:
                raise KeyError('{key} is not allowed'.format(key=key))

            if isinstance(value, datetime.datetime):
                value = value.isoformat()

            setattr(self, key, value)
