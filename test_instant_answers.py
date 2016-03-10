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


params = [(ans_type,) + case for ans_type, case_list in cases.items() for case in case_list]
idlist = ["({}) q = {!r}".format(case[0], case[1]) for case in params]

@pytest.mark.parametrize("expected_ans_type, query, expected_value", params, ids = idlist)
def test_instant_answer(expected_ans_type, query, expected_value):
    with pytest.allure.step("Make a request: q={}".format(query)):
        params = DEFAULTS.copy()
        params.update(q = query)
        req = requests.get(HOST, params = params)
        print req.url

        req.raise_for_status()

    with pytest.allure.step("Check answer type"):
        parsed_json = json.loads(req.text)
        ans_type = BeautifulSoup(parsed_json['AnswerType']).getText()
        print "AnswerType: {!r}".format(ans_type)

        assert ans_type == expected_ans_type

    with pytest.allure.step("Expecting answer: {!r}".format(expected_value)):
        ddg_value = getDDGValue(ans_type, parsed_json)
        print "Answer: {!r}".format(parsed_json["Answer"])
        print "Answer (reduced): {!r}".format(ddg_value)

        assert ddg_value == expected_value
