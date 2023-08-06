# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

from .error import SeaSmartError

BASE_URL = 'https://api.seasmart.no/v1/'

DEFAULT_API_TIMEOUT = 16


class SeaSmartApiClient(object):
    def __init__(
            self, username=None, api_key=None, timeout=None, *args, **kwargs
    ):
        if None in [username, api_key]:
            raise SeaSmartError("Authentication credentials are required.")
        self.username = username
        self.api_key = api_key
        self.url = BASE_URL
        self.timeout = timeout if timeout is not None else DEFAULT_API_TIMEOUT
        self._authentication_headers = {
            'Authorization': 'ApiKey {}:{}'.format(username, api_key)
        }

    def check_auth_headers(self):
        if self._authentication_headers is None:
            raise SeaSmartError('The API instance must be authenticated before calling this method.')

    def get_cages(self):
        '''
        Gets information about the user's cages
        '''
        self.check_auth_headers()
        cages_url = '{}/cages'.format(self.url)
        cages_response = requests.get(cages_url, headers=self._authentication_headers, timeout=self.timeout)
        if cages_response.status_code != 200:
            error = 'SeaSmart returned a non-200 response code'
            raise SeaSmartError(
                '{}: {} and error {}'.format(
                    error,
                    cages_response.status_code,
                    cages_response.text
                )
            )
        return cages_response.json()

    def get_cage(self, external_id, start=None, end=None):
        '''
        Gets information about the user's cages
        '''
        self.check_auth_headers()
        params = ''
        if start is not None or end is not None:
            params = '?'
        if start is not None:
            params = params + 'start={}&'.format(start)
        if end is not None:
            params = params + 'end={}&'.format(end)
        params = params[:-1]  # remove trailing ambersand

        cage_url = '{}/cage/{}/{}'.format(self.url, external_id, params)
        cage_response = requests.get(cage_url, headers=self._authentication_headers, timeout=self.timeout)
        if cage_response.status_code != 200:
            error = 'SeaSmart returned a non-200 response code'
            raise SeaSmartError(
                '{}: {} and error {}'.format(
                    error,
                    cage_response.status_code,
                    cage_response.text
                )
            )
        return cage_response.json()
