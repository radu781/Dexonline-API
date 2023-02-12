import requests
from bs4 import BeautifulSoup, element

from utils import BASE_LINK, SearchResult, Item
from dataclasses import dataclass


@dataclass
class Searcher:
    word: str

    def exists(self) -> bool:
        response = requests.get(BASE_LINK + self.word)
        return response.ok

    def search(self) -> list[SearchResult]:
        response = requests.get(BASE_LINK + self.word)
        soup = BeautifulSoup(response.content, "html.parser")

        words = soup.find_all("h3", attrs={"class": "tree-heading"})
        definitions = soup.find_all("div", attrs={"class": "tree-body"})
        etymologies = self.__get_etymology(soup)

        out: list[SearchResult] = []

        for word, def_ in zip(words, definitions):
            result = SearchResult()
            result.word = self.__get_word(word)
            result.plural = self.__get_plural_form(word)
            result.etymology = self.__get_etymology(def_)
            result.type = self.__get_type(word)
            result.definitions = self.__get_meanings(def_)
            out.append(result)

        return out

    def __get_word(self, word: element.Tag) -> str:
        heading = word.find_all("div")[0]
        return heading.text.split(",")[0].strip()

    def __get_plural_form(self, word: element.Tag) -> str:
        plural = ""
        for letter in word.find("span", attrs={"tree-inflected-form"}).strings:
            plural += letter
        return plural.lstrip(" ,")

    def __get_type(self, word: element.Tag) -> str:
        return word.find("span", attrs={"tree-pos-info"}).text

    def __get_meanings(self, def_: element.Tag) -> list[Item]:
        out: list[Item] = []

        type_meaning = def_.find_all("li", attrs={"class": "type-meaning"})
        for d in type_meaning:
            current_item = Item()
            current_item.meaning = d.find(
                "span", attrs={"class": "def html"}
            ).text.strip()
            # current_item.examples = self.__get_examples(d)
            current_item.synonyms = self.__get_synonyms(d)
            out.append(current_item)

        return out

    def __get_examples(self, def_: element.Tag) -> list[str]:
        out: list[str] = []

        examples = def_.find_all("li", attrs={"class": "type-example"})
        for ex in examples:
            out.append(ex.text.replace("format_quote", "").strip())
        return out

    def __get_synonyms(self, def_: element.Tag) -> list[str]:
        out: list[str] = []

        synonyms = def_.find("div", attrs={"class": "meaning-relations"}).find_all("a")
        for synonym in synonyms:
            out.append(synonym.text.strip())

        return out

    def __get_etymology(self, soup: BeautifulSoup) -> dict[str, str]:
        out: dict[str, str] = {}

        for et in soup.find_all("li", attrs={"class": "type-etymology"}):
            language_span = et.find("span", attrs={"class": "tag"}).text
            if not "limba" in language_span:
                continue
            language = language_span.replace("limba ", "")
            word = et.find("span", attrs={"class": "def html"}).text.strip()
            out[language] = word

        return out
