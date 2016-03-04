import pytest
import requests
import csv
import json
from bs4 import BeautifulSoup
import math

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json"}
    
cases = {
    "calc": [
        ("1 + 2", "3"),
        ("9*4", "36"),
        ("4/5", "0.8"),
        ("for_error", "0.8"),
    ],

    "currency_in": [
        ("currency in US", "United States Dollar (USD)"),
        ("currency in Russia", "Russian Ruble (RUB)"),
        ("currency in Sweden", "Swedish Krona (SEK)")
    ],

    "timezone_converter": [
        ("12:00 UTC+7 to MSK", "20:00 MSK (1 day prior)"),
        ("10:00 MSK to CET", "8:00 CET"),
        ("20:00 MSK to UTC", "17:00 UTC")
    ]    
}    
    
def makeRequest(query, params = dict()):
    with pytest.allure.step("Make a request: q={}".format(query)):
	params.update(q = query)
        return requests.get(HOST, params = params)

def checkType(ans_type, expected_type, query):
    if(ans_type != expected_type):
        if(ans_type == ""):
            ans_type = "type not found"
        print "Error 1 ( not ", expected_type, ")  : query = ", query, ", ans_type = ", ans_type
        return 0
    return 1
    
def checker(query, expected_value, expected_ans_type):
    params = DEFAULTS.copy()
    req = makeRequest(query, params)
    
    parsed_json = json.loads(req.text)
    # check "AnswerType"
    ans_type = BeautifulSoup(parsed_json['AnswerType']).getText()
    ct = checkType(ans_type, expected_ans_type, query)
    if(ct == 0):
        return
    
    # check "Answer"
    if(ans_type == "calc"):
        ddg_value = BeautifulSoup(parsed_json['Answer']).find('a').getText()
    else:
        ddg_value = parsed_json['Answer']
    
    with pytest.allure.step("Compare the values"):
        assert ddg_value == expected_value
    
params = cases["calc"]
@pytest.mark.parametrize("test_input, expected", params, ids = params)
def test_calc(test_input, expected):
    checker(test_input, expected, "calc")
         
params = cases["currency_in"]
@pytest.mark.parametrize("test_input, expected", params, ids = params)
def test_currency_in(test_input, expected):
    checker(test_input, expected, "currency_in")
                
params = cases["timezone_converter"]
@pytest.mark.parametrize("test_input, expected", params, ids = params)
def test_timezone_converter(test_input, expected):
    checker(test_input, expected, "timezone_converter")
        
    

    