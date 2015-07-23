# -*- coding: utf-8 -*-

try:
    import simplejson as json
except ImportError:
    import json

from ..view_models.model import ViewModel


class ApiJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ViewModel):
            return obj.__dict__

        return json.JSONEncoder.default(self, obj)
