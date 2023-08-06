from .browser import run_browser
from .wiki import search
from .wiki import get_article
from .html_convert import generate_html
from .dmenu import run_dmenu


def display(keyword):
    """
    Gets article and shows it in html viewer
    """
    content = get_article(keyword)
    content_html = generate_html(content )
    run_browser(content_html)


def main():
    """
    Runs dmenu twice, first for a keyword, then it 
    returns to offer a list from which the user can choose
    Finally it loads the article
    """
    article = None
    word = search(run_dmenu())
    if word:
        article = run_dmenu(word)
        print(article)
    if article:
        display(article)


if __name__ == '__main__':
    main()
