from .page_template import page_layout
from .css import get_css
from .text2html import ArticleContent


def generate_html(article):
    """
    generates html including css

    :param article: Article object containing title and content as plain text
    """
    content = ArticleContent(article.content)
    html =  page_layout(article.title, content, get_css())
    open("/home/marcel/test.html", "w").write(html)
    return html

