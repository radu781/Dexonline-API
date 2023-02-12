import pytest
from expected import expected_word_day, expected_word_month
from famous_word import Word


@pytest.fixture(params=expected_word_day.keys())
def day(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(params=expected_word_month.keys())
def month(request: pytest.FixtureRequest):
    return request.param


def test_day(day: tuple[int, int, int]):
    result = Word.of_the_day(day[0], day[1], day[2])
    expected_word = expected_word_day[day]["word"]
    expected_reason = expected_word_day[day]["reason"]
    assert (result.word, result.reason) == (expected_word, expected_reason)


def test_month(month: tuple[int, int]):
    result = Word.of_the_month(month[0], month[1])
    expected_word = expected_word_month[month]["word"]
    expected_reason = expected_word_month[month]["reason"]
    assert (result.word, result.reason) == (expected_word, expected_reason)
