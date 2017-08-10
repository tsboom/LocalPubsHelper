from articleutilities import *
from ArticleParser import ArticleParser, Article
import pdb

def setup():
    DOI = "10.1021/ed084p443"
    html = get_html(DOI)
    soup = soup_setup(html)
    return soup

soup = setup()

article_parser = ArticleParser(soup)

article = article_parser.parse_article()

print article.title, article.authors, article.year, article.volume, article.issue, article.toc_gif
