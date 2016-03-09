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

def makeRequest(query, params = dict()):
    with pytest.allure.step("Make a request: q={}".format(query)):
	params.update(q = query)
	print HOST, "/q=", params["q"], "/format=", params["format"]
        return requests.get(HOST, params = params)

def checkType(ans_type, expected_type, query):
    if(ans_type != expected_type):
        if(ans_type == ""):
            ans_type = "type not found"
        print "Error 1 ( not ", expected_type, ")  : query = ", query, ", ans_type = ", ans_type
        
def getDDGValue(ans_type, parsed_json):
    ddg_value = ""

    if(ans_type == "calc"):
        ddg_value = BeautifulSoup(parsed_json['Answer']).find('a').getText()
    else:
        if(ans_type == "zodiac"):
            ddg_value = parsed_json['Answer']['data']['title']
        else:
            ddg_value = parsed_json['Answer']
    
    return ddg_value
    
def checker(query, expected_value, expected_ans_type):
    params = DEFAULTS.copy()
    req = makeRequest(query, params)
    parsed_json = json.loads(req.text)
    
    # check "AnswerType"
    ans_type = BeautifulSoup(parsed_json['AnswerType']).getText()
    checkType(ans_type, expected_ans_type, query)
    
    # check "Answer"
    ddg_value = getDDGValue(ans_type, parsed_json)
    
    with pytest.allure.step("Compare the values"):
        assert ddg_value == expected_value
    
def getParams():
    params_list = []
    for c in cases.items():
        for i in range(0, len(c[1])):
            params_list.append((c[0], c[1][i][0], c[1][i][1]))
    return params_list        

@pytest.mark.parametrize("answer_type, test_input, expected", getParams())
def tests_instant_answer(answer_type, test_input, expected):
    checker(test_input, expected, answer_type)
    