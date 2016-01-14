import pytest
import requests

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json", "pretty": 1, "no_redirect": 1}

def bang_redirection_logic(bang, valid = True):
	with pytest.allure.step("make a request with BANG"):
		params = DEFAULTS.copy()
		params.update(q = "!{} query".format(bang))
		r = requests.get(HOST, params = params)
		print r.url
		r.raise_for_status()
		data = r.json()

	with pytest.allure.step("check 'Redirect' field"):
		redirect = data["Redirect"]
		print "redirected to: {}".format(redirect)

		if valid and not redirect:
			pytest.fail("expecting non-empty redirect")
		elif not valid and redirect:
			raise ValueError("expecting empty redirect")
	
	if valid:
		with pytest.allure.step("check 'Type' field"):
			assert data["Type"] == "E", "expecting Type = E (Extra)"

@pytest.mark.parametrize("bang",
						("m", "g", "ya", "imdb", "so", "a")
						)
def test_positive(bang):
	bang_redirection_logic(bang, True)

@pytest.mark.parametrize("bang",
						("yaya", "iddqd", "gibberish", "foobar", "woof")
						)
def test_negative(bang):
	bang_redirection_logic(bang, False)
	