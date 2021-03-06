"""Some queries are sensitive to regional settings (stored in cookie named `l`).
This test emulates searching wiktionary (!wt ...) with different regional settings.
Such queries lead to corresponding regional segments of `wiktionary.org`.
"""

from urllib.parse import urlparse

import pytest


@pytest.allure.feature("API - regional search")
@pytest.mark.parametrize(
    "query, cookies, expected_region",
    (
        ("!wt car", {'l': 'ru-ru'}, "ru"),
        ("!wt car", {}, "en"),
        ("!wt car", {'l': 'br-pt'}, "pt")
    )
)
def test_ddg_api_regional_search(ddg, url_params, logger, query, cookies, expected_region):
    """Check regional-specific query"""

    with pytest.allure.step("send request with q={!r} and cookies={!r} ".format(query, cookies)):

        url_params.update(q=query)
        logger.debug("With cookies: {!r}".format(cookies))
        resp = ddg.get(params=url_params, cookies=cookies)
        resp.raise_for_status()
        data = resp.json()

    with pytest.allure.step("'Redirect' contains url for regional segment of the site: {!r}".format(expected_region)):

        logger.debug("Redirect: {!r}".format(data['Redirect']))
        urlp = urlparse(data["Redirect"])
        region_id = urlp.netloc.split('.')[0]
        assert region_id == expected_region
