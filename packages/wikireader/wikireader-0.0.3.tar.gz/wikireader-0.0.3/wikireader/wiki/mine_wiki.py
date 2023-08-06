"""
Code to search wikipedia
"""
import wikipedia
from dataclasses import dataclass

@dataclass
class Article:
    title: str
    content: str
    links: list


def search(keyword):
    betterWord = wikipedia.suggest(keyword)
    if betterWord is not None:
        keyword = betterWord
        # search for the keyword
    search = wikipedia.search(keyword)
    return search


def get_article(keyword):
    """
    Gets article and returns plain text version
    """
    page = wikipedia.page(keyword)
    return Article(
        title=page.title,
        content=page.content,
        links=[])

if __name__ == '__main__':
    open('test.txt', 'w').write(get_article("Formula One"))
