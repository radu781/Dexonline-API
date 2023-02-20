import requests
from bs4 import BeautifulSoup
import random

__words: list[str] = []


def refresh() -> None:
    global __words
    BASE_LINK = "https://dexonline.ro/ajax/randomWord.php"
    result = requests.get(BASE_LINK)
    __words = result.text.split("\n")


refresh()


def random_word() -> str:
    return random.choice(__words)
