#! python2.7

import pdb
import urllib
import errno
import os
import sys
# import shutil
# import zipfile
import constants
import re
from ArticleParser import ArticleParser
from articleutilities import *

# debugging
# import pdb #use pdb.set_trace() to break


def processDOI(myDOIs):

    global results
    # create empty array to hold results dicts

    results = []

    '''
    Loop through DOIS and find info about each article. add that information to a python dictionary

    '''
    # remove empty strings from list
    myDOIs = [doi for doi in myDOIs if doi]

    for DOI in myDOIs:

        DOI = DOI.strip()

        cleanDOI= clean_doi(DOI)

        coden = get_coden(cleanDOI)
        datecode = get_datecode()

        # create image URL for PB using coden and today's date.
        img_url = ("/pb-assets/images/" + str(coden) + "/" +
                   "highlights/" + str(datecode) + "/" + str(cleanDOI) + ".jpeg")

        # create article URL
        article_link = ("/doi/" + str(DOI) + "?ref=highlight")

        # create img path for Flask, so that the images can be displayed on
        # Flask.
        img_path = "img/generated/" + coden + '/' + \
            str(datecode) + "/" + str(cleanDOI) + ".jpeg"


        # set up beautiful soup
        html = get_html(DOI)
        soup = soup_setup(html)

        # instantiate article objects
        article_parser = ArticleParser(soup)
        article = article_parser.parse_article()

        # title
        html_title = article.title

        # authors array
        authors_array = article.authors

        # join authors
        authors_joined = join_commas_and(authors_array)


        # get picture link
        gif_url = "https://pubs.acs.org" + article.toc_gif

        toc_href = gif_to_jpeg(gif_url)



        articleinfo = {
            "DOI": DOI,
            "Title": html_title,
            "article-link": article_link,
            "Authors": str(authors_joined),
            "toc_href": str(toc_href),
            "Image": img_url,
            "Flask-image-path": img_path,
            "Coden": coden,
            "Datecode": datecode,
            "Clean_doi": cleanDOI

        }

        print "\n"
        print articleinfo
        print "\n"

        results.append(articleinfo)



        # desired file name
        pathEnding = coden + '/' + str(datecode) + '/'
        filename = "app/static/img/generated/" + pathEnding + cleanDOI + '.jpeg'
        # create folder on local computer for images if doesn't exist already
        create_img_folder(pathEnding)
        try:
            download_toc_image(filename, toc_href, coden, datecode, cleanDOI)
        except:
            pass


    print results

    return results
