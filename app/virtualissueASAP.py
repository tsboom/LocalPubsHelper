
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
from datetime import datetime
from ArticleParser import ArticleParser
from articleutilities import *

# debugging
# import pdb #use pdb.set_trace() to break


def createVI(myDOIs, multiJournal, trackingCode, shortName):

    # get start time to figure out how long the process took
    startTime = datetime.datetime.now()


    global results

    # create empty array to hold results dict
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

        if multiJournal == True:
            # create image URL for PB using shortName
            shortNamePath = str(shortName) + "/"
            img_url = "/pb-assets/images/selects/" + shortNamePath + str(cleanDOI) + ".jpeg"

            # create image path for flask to display images from local folder
            img_path = "img/generated/" + shortNamePath + str(cleanDOI) + ".jpeg"

            article_link = ("/doi/abs/" + str(DOI) + str(trackingCode))
        else:
            # create image URL for PB using coden and today's date.
            codenDatePath = str(coden) + "/" + str(datecode) + "/"
            img_url = "/pb-assets/images/selects/" + codenDatePath + str(cleanDOI) + ".jpeg"
            # create img path for Flask, so that the images can be displayed on
            # Flask.
            img_path = "img/generated/" + codenDatePath + str(cleanDOI) + ".jpeg"

            # create article URL
            article_link = ("/doi/abs/" + str(DOI))

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

        # get the URL of figure 1 and set it to toc_href if there is no TOC image
        if article.toc_gif == '':
            print "\n\nno TOC image found. downloading figure 1...\n"
            try:
                fig1_gif = choose_alt_figure(article.fig_urls, "fig1")
                toc_href = gif_to_jpeg("http://pubs.acs.org" + fig1_gif)
            except:
                print "no figure 1. no image downloaded."
                toc_href = 'none'

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
        if not, create the folder and download image to it

        '''

        if multiJournal == True:
            # create folder for short journal name (groups images in a named directory)
            pathEnding = "virtualissue/" + shortNamePath
            create_img_folder(pathEnding)

            # desired filename
            filename = "app/static/img/generated/virtualissue/" + shortNamePath + cleanDOI + '.jpeg'

        else:
            # create folder for journal coden and date stamp
            pathEnding = "virtualissue/" + codenDatePath
            create_img_folder(pathEnding)

            # desired filename
            filename = "app/static/img/generated/virtualissue/" + codenDatePath + cleanDOI + '.jpeg'

        # download image
        try:
            download_toc_image(filename, toc_href, coden, datecode, cleanDOI)
        except:
            pass

        print "\n\n------------\n\n"
    time_elapsed = datetime.datetime.now() - startTime
    print "Time it took to generate a Virtual Issue: " + str(time_elapsed)  + "\n\n\n"
    return results
