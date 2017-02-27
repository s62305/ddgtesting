"""For !bang commands, the redirect will happen at the HTTP level (since that is fastest),
but it will also be returned in the content (for parsing).
If you don't want the redirect to happen in the HTTP header, use the no_redirect flag.

Relevant return field:
Redirect: !bang redirect URL

More at https://api.duckduckgo.com/api
"""

import pytest


@pytest.allure.feature("API - bang queries")
@pytest.allure.story("real bang name")
@pytest.mark.parametrize(
    "bang_name",
    ("m", "g", "ya", "imdb", "so", "a")
)
def test_ddg_api_bang_positive(ddg, url_params, logger, bang_name):
    """Test query with a real bang"""

    with pytest.allure.step("send request with REAL bang"):

        url_params.update(q="!{bang} query".format(bang=bang_name))
        r = ddg.get(params=url_params)
        r.raise_for_status()
        data = r.json()

    with pytest.allure.step("'Type' in the response is 'E'"):

        assert data['Type'] == 'E'

    with pytest.allure.step("'Redirect' in the response IS NOT empty"):

        logger.debug("Will be redirected to: {!r}".format(data['Redirect']))
        assert data['Redirect']


@pytest.allure.feature("API - bang queries")
@pytest.allure.story("invalid bang name")
@pytest.mark.parametrize(
    "bang_name",
    ("yaya", "iddqd", "gibberish", "foobar", "woof")
)
def test_ddg_api_bang_negative(ddg, url_params, logger, bang_name):

    with pytest.allure.step("send request with FALSE bang"):

        url_params.update(q="!{bang} query".format(bang=bang_name))
        r = ddg.get(params=url_params)
        r.raise_for_status()
        data = r.json()

    with pytest.allure.step("'Redirect' in the response IS empty"):

        logger.debug("Redirect: {!r}".format(data['Redirect']))
        assert not data['Redirect']
