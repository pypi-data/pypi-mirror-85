# seasmart-python-api-client

[![PyPI version](https://badge.fury.io/py/seasmart-python-api-client.svg)](https://pypi.org/project/seasmart-python-api-client/)

<a href="https://github.com/SeaSmart/seasmart-python-api-client/actions"><img alt="GitHub Actions status" src="https://github.com/SeaSmart/seasmart-python-api-client/workflows/python-tests/badge.svg"></a>

A very incomplete Python client library for the SeaSmart API.

## Setup

    pip install seasmart-python-api-client

## Example Usage

    from SeaSmartApiClient.api import SeaSmartApiClient

    seasmart = SeaSmartApiClient(
        username="test_username",
        api_key="test_api_key"
    )
    cages = seasmart.get_cages()

## Contributing

Information on [contributing](https://github.com/SeaSmart/seasmart-python-api-client/blob/master/CONTRIBUTING.md) to this python library.

## Testing

To run the tests,

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pytest
    deactivate

to run the tests for this project.
