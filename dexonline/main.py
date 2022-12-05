import pprint

from dexonline.searcher import Searcher


def main():
    s = Searcher("test")
    pprint.pprint(s.search())


if __name__ == "__main__":
    main()
