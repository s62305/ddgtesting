import pytest
import logging
import requests
from common import BaseClient


def pytest_addoption(parser):
    parser.addoption("--endpoint", action="store", default="https://api.duckduckgo.com/", help="DDG API endpoint")


def pytest_report_header(config):
    return (
        "API: " + config.getoption('endpoint'),
    )


@pytest.fixture(autouse=True, scope='session')
def logger():
    '''Global logging settings
    '''
    logging.basicConfig(level=logging.DEBUG)
    return logging

@pytest.fixture(scope='session')
def api_endpoint(request):
    endp = request.config.getoption('endpoint')
    r = requests.head(endp)
    r.raise_for_status()
    return endp

@pytest.fixture(scope='function')
def url_params():
    '''Default url params
    '''
    return {
        'format': 'json',
        'no_redirect': 1
    }

@pytest.fixture()
def ddg(api_endpoint):
    return BaseClient(api_endpoint)
