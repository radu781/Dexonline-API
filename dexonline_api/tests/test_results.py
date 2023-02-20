import pytest
from expected import expected_result
from searcher import Searcher
from utils import SearchResult


@pytest.fixture(params=expected_result.keys())
def searcher(request: pytest.FixtureRequest) -> tuple[str, list[SearchResult]]:
    word = request.param
    search_results = Searcher(word).search()
    return (word, search_results)


def test_result_len(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    assert len(result) == len(expected_result[word])


def test_result_words(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_word = [sr.word for sr in result]
    expected_word = [w["word"] for w in expected_result[word]]
    assert actual_word == expected_word


def test_result_plurals(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_plural = [sr.plural for sr in result]
    expected_plural = [w["plural"] for w in expected_result[word]]
    assert actual_plural == expected_plural


def test_result_types(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_types = [sr.type for sr in result]
    expected_types = [w["type"] for w in expected_result[word]]
    assert actual_types == expected_types


def test_result_etymology(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_etymology = [sr.etymology for sr in result]
    expected_etymology = [w["etymology"] for w in expected_result[word]]
    assert actual_etymology == expected_etymology


def test_synonyms(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_synonyms = [[syn.synonyms for syn in sr.definitions] for sr in result]
    expected_synonyms = [
        [syn["synonyms"] for syn in w["definitions"]] for w in expected_result[word]
    ]
    assert actual_synonyms == expected_synonyms


def test_meaning(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_meaning = [[mn.meaning for mn in sr.definitions] for sr in result]
    expected_meaning = [
        [syn["meaning"] for syn in w["definitions"]] for w in expected_result[word]
    ]
    assert actual_meaning == expected_meaning


def test_sub_meaning(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_sub_meaning = [[ex.sub_meaning for ex in sr.definitions] for sr in result]
    expected_sub_meaning = [
        [syn["sub_meaning"] for syn in w["definitions"]] for w in expected_result[word]
    ]
    assert actual_sub_meaning == expected_sub_meaning


def test_examples(searcher: tuple[str, list[SearchResult]]):
    word, result = searcher
    actual_examples = [[ex.examples for ex in sr.definitions] for sr in result]
    expected_examples = [
        [syn["examples"] for syn in w["definitions"]] for w in expected_result[word]
    ]
    assert actual_examples == expected_examples
