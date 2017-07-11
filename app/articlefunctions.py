global coden
import constants
from bs4 import BeautifulSoup
import requests as r
import pdb

# debugging
# import pdb #use pdb.set_trace() to break

#constants
DOI_PREFIX = 'http://pubs.acs.org/doi/full/'
# no figures DOI = "10.1021/acs.accounts.7b00142"
DOI = "10.1021/acs.accounts.6b00581"
#enhanced figures DOI
#DOI = "10.1021/jacs.7b03655"


def get_html(DOI):
    html = r.get(DOI_PREFIX + DOI).text
    # check if html is the actual article, and not an error page!!!
    return html
#
# def validateDOI(DOI):
#     if

def soup_setup(html):
    html = html.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def look_up_coden(DOI):
    cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
    journalprefix = cleanDOI[:-7]
    coden = constants.CODEN_MATCH[journalprefix]
    return coden;


def get_title(soup):
    title = soup.find('span', {'class': 'hlFld-Title'})
    return title.text.encode('utf-8')


# def get_toc_image(DOI):

#


def get_authors(soup):
    authors_soup = soup.select('#authors > span.hlFld-ContribAuthor')
    author_names = []
    for author in authors_soup:
        name_tag = author.find('span', {'class': 'hlFld-ContribAuthor'})
        authors_tag = name_tag.contents[0]
        author_name = authors_tag.contents
        entire_name_symbols = author.text.strip()
        # check to see if a star is in the entire name,
        # then add the star to the name only
        if '*' in entire_name_symbols:
            author_name = author_name[0] + '*'
        else:
            author_name = author_name[0]
        author_name.encode('utf-8')
        author_names.append(author_name)
    return author_names

def join_commas_and(authors):
    # join correctly formatted authors
    # add ', ' and 'and'
    if len(authors)==2:
            authors.insert(1, ' and ')
            authors_joined = (''.join(authors))
    elif len(authors)==1:
        authors_joined = (''.join(authors))
    else:
        all_but_last = ', '.join(authors[:-1])
        last = authors[-1]
        authors_joined = ', and '.join([all_but_last, last])
    return authors_joined

def get_citation_year(soup):
    citation_year = soup.find('span', {'class': 'citation_year'})
    return citation_year.text.encode('utf-8')


def get_citation_volume(soup):
    citation_volume = soup.find('span', {'class': 'citation_volume'})
    return citation_volume.text.encode('utf-8')

def get_citation_issue(soup):
    issue_info = soup.find("span", class_="citation_volume").next_sibling
    return issue_info.encode("utf-8")

# def download_toc_image(DOI):


def run(DOI):
    html = get_html(DOI)
    soup = soup_setup(html)
    title = get_title(soup)
    year = get_citation_year(soup)
    volume = get_citation_volume(soup)
    issue = get_citation_issue(soup)
    author_names = get_authors(soup)
    authors_joined = join_commas_and(author_names)
    print title
    print year, volume, issue
    print authors_joined


run(DOI)
