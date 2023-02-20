import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from utils import DexOnlineException


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
        word_line = soup.find("span", attrs={"class": "def"})
        if word_line is None:
            raise DexOnlineException("Word definition not found")
        word_line = "".join(word_line.strings).strip()
        word = re.split(r"[,\s]", word_line)[0].strip()

        reason_line = soup.find("div", attrs={"class": "card-footer"})
        if reason_line is None:
            raise DexOnlineException("Word choice reason not found")
        reason = "".join(reason_line.strings).removeprefix(" Cheia alegerii: ").strip()

        return WordWrapper(word, reason)
