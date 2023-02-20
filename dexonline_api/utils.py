from dataclasses import dataclass, field

BASE_LINK = "https://dexonline.ro/definitie/"


@dataclass
class Item:
    synonyms: list[str] = field(default_factory=list)
    meaning: str = field(default="")
    examples: list[str] = field(default_factory=list)
    sub_meaning: list[str] = field(default_factory=list)


@dataclass()
class SearchResult:
    word: str = field(default="")
    plural: str = field(default="")
    type: str = field(default="")
    definitions: list[Item] = field(default_factory=list)
    etymology: dict[str, str] = field(default_factory=dict)


class DexOnlineException(Exception):
    ...
