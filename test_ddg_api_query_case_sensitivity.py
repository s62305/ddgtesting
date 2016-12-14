import pytest
import json

'''Queries can be case sensitive e.g. blackberry (API example) vs BlackBerry (API example).
In the first case (lowercase blackberry) it returns a disambiguation page;
in the latter case (MixedCase BlackBerry) it returns info primarily about the device (inferring what you meant from the case).
'''

@pytest.allure.feature("API - query case sensitivity")
@pytest.allure.story("case sensitive query")
@pytest.mark.parametrize(
    "query",
    ("DreamWorks", "BlackBerry", "AC/DC")
)
def test_ddg_api_case_sensitive_query(ddg, url_params, logger, query):
    with pytest.allure.step("Send request: q={!r}".format(query)):
        url_params.update(q=query)
        r = ddg.get(params=url_params)
        r.raise_for_status()
        data_original = r.json()
        # logger.debug("\nOriginal response:\n{!r}".format(data_original))
        pytest.allure.attach("original_response.json", json.dumps(data_original, indent=4), pytest.allure.attach_type.JSON)
    
    query_lower = query.lower()

    with pytest.allure.step("Send request: q={!r}".format(query_lower)):
        url_params.update(q=query_lower)
        r = ddg.get(params=url_params)
        r.raise_for_status()
        data_lower = r.json()
        # logger.debug("\nResponse for lower case query:\n{!r}".format(data_lower))
        pytest.allure.attach("lower_case_response.json", json.dumps(data_lower, indent=4), pytest.allure.attach_type.JSON)

    with pytest.allure.step("Two responses are different"):
        assert data_lower != data_original


@pytest.allure.feature("API - query case sensitivity")
@pytest.allure.story("case insensitive query")
@pytest.mark.parametrize(
    "query",
    ("Apple", "Copacabana", "Moscow", "DNA")
)
def test_ddg_api_case_insensitive_query(ddg, url_params, logger, query):
    with pytest.allure.step("Send request: q={!r}".format(query)):
        url_params.update(q=query)
        r = ddg.get(params=url_params)
        r.raise_for_status()
        data_original = r.json()
        # logger.debug("\nOriginal response:\n{!r}".format(data_original))
        pytest.allure.attach("original_response.json", json.dumps(data_original, indent=4), pytest.allure.attach_type.JSON)
    
    query_lower = query.lower()

    with pytest.allure.step("Send request: q={!r}".format(query_lower)):
        url_params.update(q=query_lower)
        r = ddg.get(params=url_params)
        r.raise_for_status()
        data_lower = r.json()
        # logger.debug("\nResponse for lower case query:\n{!r}".format(data_lower))
        pytest.allure.attach("lower_case_response.json", json.dumps(data_lower, indent=4), pytest.allure.attach_type.JSON)

    with pytest.allure.step("Two responses are the same"):
        assert data_lower == data_original
