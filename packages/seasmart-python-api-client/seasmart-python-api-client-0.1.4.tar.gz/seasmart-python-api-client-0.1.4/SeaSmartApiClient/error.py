# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class SeaSmartError(Exception):
    '''
        This base error will help determine when the SeaSmart API returns a bad
        response or otherwise raises an exception while using the API.
    '''
    pass
