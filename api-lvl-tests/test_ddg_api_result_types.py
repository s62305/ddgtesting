"""Relevant return field:
Type: response category, i.e.
    A (article),
    D (disambiguation),
    C (category),
    N (name),
    E (exclusive),
    or nothing.
More at https://api.duckduckgo.com/api
"""

import pytest


@pytest.allure.feature("API - result types")
@pytest.mark.parametrize(
    "query, expected_type",
    (
        ("apple", "D"),
        ("!so python3", "E"),
        ("Morse code", "A"),
        ("Poetry by William Shakespeare", "C")
    )
)
def test_ddg_api_result_type(ddg, url_params, logger, query, expected_type):
    """Check result type for a query"""

    with pytest.allure.step("send request"):

        url_params.update(q=query)
        resp = ddg.get(params=url_params)
        resp.raise_for_status()
        data = resp.json()

    with pytest.allure.step("'Type' in the response is {!r}".format(expected_type)):

        logger.debug("Expected Type: {!r}".format(expected_type))
        logger.debug("Actual Type: {!r}".format(data['Type']))
        assert expected_type == data['Type']
