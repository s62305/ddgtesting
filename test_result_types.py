import pytest
import requests

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json", "pretty": 1, "no_redirect": 1}

@pytest.mark.parametrize("query, expected_type",
						[("apple", "D"),
						("!so python3", "E"),
						("Morse code", "A"),
						("Poetry by William Shakespeare", "C")]
						)
def test_positive(query, expected_type):
	with pytest.allure.step("make a request"):
		params = DEFAULTS.copy()
		params.update(q = query)
		r = requests.get(HOST, params = params)
		print r.url

		r.raise_for_status()
		data = r.json()

	with pytest.allure.step("check 'Type' field with expected value ({})".format(expected_type)):
		print "Type: {}".format(data["Type"])
		assert expected_type == data["Type"], "Unexpected type: {}".format(data["Type"])