import logging

import pytest
import requests

from common import BaseClient


def pytest_addoption(parser):

    parser.addoption(
        "--endpoint",
        action="store",
        default="https://api.duckduckgo.com/",
        help="DDG API endpoint"
    )


def pytest_report_header(config):

    return (
        "API: " + config.getoption('endpoint'),
    )


@pytest.fixture(autouse=True, scope='session')
def logger():
    """Global logging settings"""

    logging.basicConfig(level=logging.DEBUG)
    return logging


@pytest.fixture(scope='session')
def api_endpoint(request):
    """API endpoint (URL)"""

    endp = request.config.getoption('endpoint')
    resp = requests.head(endp)
    resp.raise_for_status()
    return endp


@pytest.fixture(scope='function')
def url_params():
    """Default url params"""

    return {
        'format': 'json',
        'no_redirect': 1
    }


@pytest.fixture()
def ddg(api_endpoint):
    """HTTP client instance"""

    return BaseClient(api_endpoint)
