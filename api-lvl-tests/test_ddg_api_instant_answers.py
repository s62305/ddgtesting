"""Our instant answers come from a variety of sources, including
Wikipedia, Wikia, CrunchBase, GitHub, WikiHow, The Free Dictionary – over 100 in total.

Our long-term goal is for all of our instant answers to be available through this open API.
Many of these instant answers are open source via our DuckDuckHack platform.
Using that platform, you can add your own APIs and data sources as well.

More at https://api.duckduckgo.com/api
"""

import pytest


@pytest.allure.feature("API - instant answers")
@pytest.mark.parametrize(
    "expected_ans_type, query, expected_value",
    (
        ("currency_in", "currency in US", "United States Dollar (USD)"),
        ("currency_in", "currency in Russia", "Russian Ruble (RUB)"),
        ("currency_in", "currency in Sweden", "Swedish Krona (SEK)"),
        ("timezone_converter", "10:00 MSK to CET", "8:00 CET"),
        ("timezone_converter", "20:00 MSK to UTC", "17:00 UTC"),
        ("zodiac", "zodiac 21st June", "Gemini"),
        ("zodiac", "zodiac 1st July", "Cancer"),
        ("zodiac", "zodiac 29st August", "Virgo")
    )
)
def test_instant_answer(ddg, url_params, logger, expected_ans_type, query, expected_value):

    with pytest.allure.step("send request: {!r}".format(query)):

        url_params.update(q=query)
        r = ddg.get(params=url_params)
        r.raise_for_status()

    with pytest.allure.step("'AnswerType' in the response is {!r}".format(expected_ans_type)):

        data = r.json()
        ans_type = data['AnswerType']
        logger.debug("Expected AnswerType: {!r}".format(expected_ans_type))
        logger.debug("Actual AnswerType: {!r}".format(ans_type))
        assert ans_type == expected_ans_type

    with pytest.allure.step("'Answer' in the response is {!r}".format(expected_value)):

        answer = data['Answer']
        logger.debug("Raw answer: {!r}".format(data['Answer']))
        logger.debug("Processed answer: {!r}".format(answer))
        assert answer == expected_value
