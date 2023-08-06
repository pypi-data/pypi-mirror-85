from .page_template import page_layout
from .text2html import ArticleContent
from .. import conf


def generate_html(article):
    """
    generates html including css

    :param article: Article object containing title and content as plain text
    """
    content = ArticleContent(article.content)
    html =  page_layout(article.title, content, conf.css)
    return html

