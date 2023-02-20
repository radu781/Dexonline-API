from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup, NavigableString, element
from utils import BASE_LINK, DexOnlineException, Item, SearchResult


@dataclass
class Searcher:
    word: str
    response: requests.Response | None = field(init=False, default=None)

    def exists(self) -> bool:
        if self.response is None:
            self.response = requests.get(BASE_LINK + self.word)
        return self.response.ok

    def search(self) -> list[SearchResult]:
        if self.response is None:
            self.response = requests.get(BASE_LINK + self.word)
        soup = BeautifulSoup(self.response.content, "html.parser")

        words = soup.find_all("h3", attrs={"class": "tree-heading"})
        definitions = soup.find_all("div", attrs={"class": "tree-body"})

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
        plural_line = word.find("span", attrs={"tree-inflected-form"})
        if plural_line is None:
            raise DexOnlineException("Plural form not found")

        plural = "".join([letter for letter in plural_line.strings])
        return plural.lstrip(" ,")

    def __get_type(self, word: element.Tag) -> str:
        type_line = word.find("span", attrs={"tree-pos-info"})
        if type_line is None:
            raise DexOnlineException("Type not found")
        return type_line.text

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

        meanings = def_.find("div", attrs={"class": "meaning-relations"})
        if isinstance(meanings, NavigableString) or meanings is None:
            raise DexOnlineException("Could not find synonyms", meanings)
        synonyms = meanings.find_all("a")
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
