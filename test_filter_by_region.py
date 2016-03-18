import pytest
import requests
import json
from urlparse import urlparse

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json", "no_redirect": 1}
    
params_list = [("!wt car", {'l': 'ru-ru'}, "ru"),
               ("!wt car", {}, "en"),
               ("!wt car", {'l': 'br-pt'}, "pt")              
              ]

@pytest.mark.parametrize("query, cookies, expected_region", params_list, ids = params_list)
def test_filter_by_region(query, cookies, expected_region):
    with pytest.allure.step("Make a request: q={}".format(query)):
        params = DEFAULTS.copy()
        params.update(q = query)
        req = requests.get(HOST, params = params, cookies = cookies)
        print "url: ", req.url, ", cookies: ", cookies

        req.raise_for_status()
        
    with pytest.allure.step("Expected region: {}".format(expected_region)):
        urlp = urlparse(req.json()["Redirect"])
        ddg_region = urlp.netloc.split('.')[0]
        print "DDGRegion: {!r}".format(ddg_region)
        
        assert ddg_region == expected_region
