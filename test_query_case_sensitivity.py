import pytest
import requests

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json", "pretty": 1, "no_redirect": 1}

def make_request(query, params = dict()):
	with pytest.allure.step("Make a request: q={}".format(query)):
		params.update(q = query)
		return requests.get(HOST, params = params)

def check_case_sensitivity(query, sensitive = True):
	params = DEFAULTS.copy()

	r1 = make_request(query, params)
	print query, ":", r1.url

	query = query.lower()
	r2 = make_request(query, params)
	print query, ":", r2.url

	with pytest.allure.step("Compare responses"):
		if sensitive:
			assert r1.json() != r2.json()
		else:
			assert r1.json() == r2.json()

@pytest.mark.parametrize("query",
						["DreamWorks", "BlackBerry", "AC/DC"]
						)
def test_sensitive(query):
	check_case_sensitivity(query, True)

@pytest.mark.parametrize("query",
						["Apple", "Copacabana", "Moscow", "DNA"]
						)
def test_insensitive(query):
	check_case_sensitivity(query, False)