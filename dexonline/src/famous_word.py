import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import re

@dataclass
class WordWrapper:
    word: str
    reason: str


class Word:
    @staticmethod
    def of_the_day(year: int, month: int, day: int) -> WordWrapper:
        BASE_LINK = "https://dexonline.ro/cuvantul-zilei/"
        link = BASE_LINK + f"{year}/{month:02}/{day:02}"
        return Word.__search(link)

    @staticmethod
    def of_the_month(year: int, month: int) -> WordWrapper:
        BASE_LINK = "https://dexonline.ro/cuvantul-lunii/"
        link = BASE_LINK + f"{year}/{month:02}"
        return Word.__search(link)

    @staticmethod
    def __search(link: str) -> WordWrapper:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        word = "".join(soup.find("span", attrs={"class": "def"}).strings).strip()
        word = re.split(r"[,\s]", word)[0].strip()

        reason = (
            "".join(soup.find("div", attrs={"class": "card-footer"}).strings)
            .removeprefix(" Cheia alegerii: ")
            .strip()
        )
        return WordWrapper(word, reason)
