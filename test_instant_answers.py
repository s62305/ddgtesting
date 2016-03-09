import pytest
import requests
import json
from bs4 import BeautifulSoup

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json"}
    
cases = {
    "calc": [
        ("1 + 2", "3"),
        ("9*4", "36"),
        ("4/5", "0.8")
        #("for_error", "0.8")
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
        ],

    "zodiac": [
        ("zodiac 21st June", "Gemini"),
        ("zodiac 1st July", "Cancer"),
        ("zodiac 29st August", "Virgo")
        ]
}    

def getDDGValue(ans_type, parsed_json):
    ddg_value = parsed_json['Answer']
    
    if(ans_type == "calc"):
        ddg_value = BeautifulSoup(ddg_value).find('a').getText()
    elif(ans_type == "zodiac"):
        ddg_value = ddg_value['data']['title']
        
    return ddg_value

params = [(k,) + item for k, v in cases.items() for item in v]

@pytest.mark.parametrize("expected_ans_type, query, expected_value", params)
def tests_instant_answer(expected_ans_type, query, expected_value):

    with pytest.allure.step("Make a request: q={}".format(query)):
        params = DEFAULTS.copy()
        params.update(q = query)
        req = requests.get(HOST, params = params)
        print req.url
        
    with pytest.allure.step("Check answer type"):
        parsed_json = json.loads(req.text)
        ans_type = BeautifulSoup(parsed_json['AnswerType']).getText()
        assert ans_type == expected_ans_type
        
    ddg_value = getDDGValue(ans_type, parsed_json)
    
    with pytest.allure.step("Compare the values"):
        assert ddg_value == expected_value
    