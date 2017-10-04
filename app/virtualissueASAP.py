
from bs4 import BeautifulSoup
import constants
import pdb
import urllib
import csv
import os
import sys
import shutil
import zipfile
import errno
import re
import datetime
from ArticleParser import ArticleParser
from articleutilities import *

# debugging
# import pdb #use pdb.set_trace() to break


def createVI(myDOIs):

    global results

    # create empty array to hold results dicts
    results = []

    '''
    Loop through the DOIS to find information from each article page. add that info to lists.

    '''
    clean_journal = []

    # remove empty strings from list
    myDOIs = [doi for doi in myDOIs if doi]

    for DOI in myDOIs:

        DOI = DOI.strip()

        cleanDOI= clean_doi(DOI)

        coden = get_coden(cleanDOI)
        datecode = get_datecode()

        # create image URL for PB using coden and today's date.
        img_url = ("/pb-assets/images/selects/" + str(coden) +
                   "/" + str(datecode) + "/" + str(cleanDOI) + ".jpeg")

        # create article URL
        article_link = ("/doi/abs/" + str(DOI))

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


        # get link to the toc image
        gif_url = "https://pubs.acs.org" + article.toc_gif

        toc_href = gif_to_jpeg(gif_url)


        # get journal name
        journal = article.journal


        """
            I'm not sure about this next part. Should i do an if/else liek this? The process should be different depending on if
            the article is an Article ASAP or not. My program puts "Article ASAP" inside of the view template. which is bad I think.
        """
        # check to see if article is an Article ASAP
        journal_string = soup.select('#citation')[0].text
        if "Article ASAP" not in journal_string:
            # get citation year
            year = article.year

            # get citation volume
            volume = article.volume

            # get issue info and pages
            issue_info = article.issue

        else:
            year = ''
            volume = ''
            issue_info = ''

        articleinfo = {
            'DOI': DOI,
            'Title': html_title,
            'article-link': article_link,
            'Authors': str(authors_joined),
            'toc_href': str(toc_href),
            'Image': img_url,
            'Journal': journal,
            'Volume': volume,
            'Issue-info': issue_info,
            'Year': year,
            "Datecode": datecode,
            "Clean_doi": cleanDOI,
            'Coden': coden
            }

        print "\n" + str(articleinfo) + "\n"
        results.append(articleinfo)

        '''
        check to see if there is an existing folder for coden and date,
        if not, create the folder

        '''
        # create folder for journal coden and date stamp
        try:

            os.makedirs("app/static/img/generated/virtualissue/" + coden + '/' + \
                str(datecode) + "/")

        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise exc
            pass

        # desired filename
        filename = "app/static/img/generated/virtualissue/" + coden + '/' + \
        str(datecode) + "/" + cleanDOI + '.jpeg'
        try:
            download_toc_image(filename, toc_href, coden, datecode, cleanDOI)
        except:
            pass


        # '''
        # ZIP images using shutil
        #
        # '''
        # filedirectory = "app/static/img/generated/virtualissue/" + \
        #     coden + '/' + str(datecode) + "/"
        #
        # shutil.make_archive(datecode, 'zip', filedirectory)
        # shutil.copy(datecode + '.zip', filedirectory)

    return results
