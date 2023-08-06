# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import mock

from unittest import TestCase
from SeaSmartApiClient.api import SeaSmartApiClient, BASE_URL
from SeaSmartApiClient.error import SeaSmartError


def default_api():
    return SeaSmartApiClient(
        username="test_username",
        api_key="test_api_key",
        timeout=5
    )


class TestSeaSmartAPI(TestCase):
    def setUp(self):
        self.api = default_api()

    def test_get_cages(self):
        # success case
        with mock.patch('SeaSmartApiClient.api.requests') as mock_request:
            mock_get = mock.Mock()
            mock_get.status_code = 200
            mock_get.json.return_value = {}
            mock_request.get.return_value = mock_get

            self.api.get_cages()

            cages_url = '{}/cages'.format(BASE_URL)
            mock_request.get.assert_any_call(cages_url, headers=self.api._authentication_headers, timeout=5)

        # error case (not found)
        with mock.patch('SeaSmartApiClient.api.requests') as mock_request:
            mock_get = mock.Mock()
            mock_get.status_code = 404
            mock_get.json.return_value = {}
            mock_request.get.return_value = mock_get

            with self.assertRaises(SeaSmartError):
                self.api.get_cages()
