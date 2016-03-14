import pytest
import requests
import json
from bs4 import BeautifulSoup
from urlparse import urlparse

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json", "no_redirect": 1}
    
params_list = [("!wt car", {'l': 'ru-ru'}, "ru"),
               ("!wt car", {'l': ''}, "en"),
               ("!wt car", {'l': 'br-pt'}, "pt")              
              ]

@pytest.mark.parametrize("query, cookies, expected_region", params_list, ids = params_list)
def test_filter_by_region(query, cookies, expected_region):
    with pytest.allure.step("Make a request: q={}".format(query)):
        params = DEFAULTS.copy()
        params.update(q = query)
        req = requests.get(HOST, params = params, cookies = cookies)
        print req.url

        req.raise_for_status()
        
    with pytest.allure.step("Check region"):
        urlp = urlparse(str(req.json()["Redirect"]))
        ddg_region = str(urlp.netloc)[0] + str(urlp.netloc)[1]
        print "DDGRegion: {!r}".format(ddg_region)
        
        assert ddg_region == expected_region
