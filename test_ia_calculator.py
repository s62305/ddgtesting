import pytest
import requests
import csv
import json
from bs4 import BeautifulSoup
import math

HOST = "http://api.duckduckgo.com"
DEFAULTS = {"format": "json"}
    
def make_request(query, params = dict()):
    with pytest.allure.step("Make a request: q={}".format(query)):
	params.update(q = query)
        return requests.get(HOST, params = params)

def calculate(query, expected_value):
    params = DEFAULTS.copy()
    req = make_request(query, params)
    
    parsed_json = json.loads(req.text)
    ddg_counted_value = BeautifulSoup(parsed_json['Answer']).find('a').getText()
    
    ddg_counted_value_list = ddg_counted_value.split(' ')
    
    with pytest.allure.step("Compare the values"):
        if query[0] == 'l':
            assert ("%.6f" % (float(expected_value))) == ("%.6f" % (float(ddg_counted_value)))
        else:
            if len(ddg_counted_value_list) == 1: # if ddg_counted_value is one number 
                assert ddg_counted_value == expected_value
            else: # if ddg_counted_value is long number
                ddg_counted_value = float(ddg_counted_value_list[0]) * pow(int(ddg_counted_value_list[2]) / 100, int(ddg_counted_value_list[2]) % 100)
                assert ddg_counted_value == expected_value
                
    
    
@pytest.mark.parametrize("test_input, expected", [({'q' : '1+2'}, '3'), ({'q' : '2-3'}, '-1'), ({'q' : '3*2'}, '6'), ({'q' : '10/2'}, '5')])
def test_calculator_trivial(test_input, expected):
    ddg_counted_value = calculate(test_input.get('q'), expected)

@pytest.mark.parametrize("test_input, expected", [({'q' : '10000000000000000000000001 + 21111111111111111111111111111111'}, 10000000000000000000000001 + 21111111111111111111111111111111)])
def test_calculator_long(test_input, expected):
    ddg_counted_value = calculate(test_input.get('q'), expected)
    
@pytest.mark.parametrize("test_input, expected", [({'q' : 'fact(3)'}, '6'), ({'q' : 'fact(5)'}, '120'), ({'q' : 'fact(7)'}, '5,040'), ({'q' : 'fact(10)'}, '3,628,800')])
def test_calculator_factorial(test_input, expected):
    ddg_counted_value = calculate(test_input.get('q'), expected)
    
@pytest.mark.parametrize("test_input, expected", [({'q' : 'log(1)'}, '0'), ({'q' : 'log(10)'}, '1'), ({'q' : 'log(100)'}, '2'), ({'q' : 'log(5)'}, '0.698970')])
def test_calculator_log(test_input, expected):
    ddg_counted_value = calculate(test_input.get('q'), expected)
    
@pytest.mark.parametrize("test_input, expected", [({'q' : 'ln(1)'}, 0), ({'q' : 'ln(3)'}, math.log(3)), ({'q' : 'ln(100)'}, math.log(100)), ({'q' : 'ln(5)'}, math.log(5))])
def test_calculator_ln(test_input, expected):
    ddg_counted_value = calculate(test_input.get('q'), expected)        
    