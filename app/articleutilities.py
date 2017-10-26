global coden
import constants
from bs4 import BeautifulSoup
import requests as r
import pdb
import urllib
import datetime
import os
import errno

# debugging
# import pdb #use pdb.set_trace() to break

def get_html(DOI):
    html = r.get(constants.DOI_PREFIX + DOI).text
    # check if html is the actual article, and not an error page!!!
    return html

def soup_setup(html):
    html = html.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def clean_doi(DOI):
    cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
    return cleanDOI

def get_coden(cleanDOI):
    journalprefix = cleanDOI[:-7]
    coden = constants.CODEN_MATCH[journalprefix]
    return coden;

def get_datecode():
    date = datetime.date.today()
    datecode = datetime.datetime.now().strftime("%Y%m%d")
    return datecode




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





# this function gets reused for each image (if you are on the VPN)
def gif_to_jpeg(gif):
    # get the large jpeg version of image based on URL string
    if "medium" in gif:
        image_url = gif.replace('medium', 'large')
        image_url = image_url.replace('.gif', '.jpeg')
        return image_url
    else:
        return gif




def create_img_folder(pathEnding):
    try:
        os.makedirs("app/static/img/generated/" + pathEnding)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
        pass

def download_toc_image(filename, toc_href, coden, datecode, cleanDOI):
    if toc_href.endswith('.jpeg'):
        filename = filename + '.jpeg'
    else:
        filename = filename + '.gif'

    #download image using urllib
    urllib.urlretrieve(toc_href, filename)
    print cleanDOI + ' IMAGE DOWNLOADED'


def setup():
    DOI = "10.1021/jacs.7b04930"
    html = get_html(DOI)
    soup = soup_setup(html)
    return soup
