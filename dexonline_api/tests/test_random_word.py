from dexonline_api import random_word

def test_random_word():
    for _ in range(5):
        assert random_word() != ""
