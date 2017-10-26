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
        #remove new lines
        rawDOI = DOI.strip()




        # deal with custom figures other than the TOC image

        # check to see if there's extra figure code at the end of the DOI and separate it out
        if ' ' in rawDOI:
            hasAltFigure = True;
            # get the actual DOI from rawDOI
            DOI = rawDOI.rsplit(' ')[0]
            # get the code at the end of the DOI after the space
            figCode = rawDOI.rsplit(' ')[1]
            # get number out of the code
            figNumber = ''.join([i for i in figCode if i.isdigit()])

        else:
            DOI = rawDOI


        # set up beautiful soup
        html = get_html(DOI)
        soup = soup_setup(html)

        # instantiate article objects
        article_parser = ArticleParser(soup)
        article = article_parser.parse_article()


        # create img URL paths
        cleanDOI= clean_doi(DOI)

        coden = get_coden(cleanDOI)
        datecode = get_datecode()

        # create image URL for PB using coden and today's date.
        img_url = ("/pb-assets/images/" + str(coden) + "/" +
                   "highlights/" + str(datecode) + "/" + str(cleanDOI) + ".jpeg")

        # create article URL
        article_link = ("/doi/" + str(DOI) + "?ref=highlight")

        # title
        html_title = article.title

        # authors array
        authors_array = article.authors

        # join authors
        authors_joined = join_commas_and(authors_array)


        # get picture link
        gif_url = "https://pubs.acs.org" + article.toc_gif

        toc_href = gif_to_jpeg(gif_url)
        # set other href to nothing in case there is no other image needed
        other_href = ''

        # create TOC img path for Flask, so that the images can be displayed on
        # Flask.
        img_path = "img/generated/" + coden + '/' + \
            str(datecode) + "/" + str(cleanDOI) + ".jpeg"

        # get picture link for alternative images to toc_href using figCode and figNumber
        if hasAltFigure == True:
            if "F" in figCode:
                fig_id = "fig" + figNumber
                other_gif = article.get_other_gif(fig_id)
                print "figure gif url" + other_gif
            elif "S" in figCode:
                fig_id = "sch" + figNumber
                other_gif = article.get_other_gif(fig_id)
                print "scheme gif: " + other_gif
            elif "E" in figCode:
                # for editors choice
                ecHTML = "<div class=\"ec-article\"><img src=\"/pb-assets/images/editorschoice/ec-article.gif\"></div>"
                print "ec test"
            elif "C" in figCode:
                # for the chart
                fig_id = "cht" + figNumber
                other_gif = article.get_other_gif(fig_id)
                print "chart gif: " + other_gif

            # get the jpeg out of the gif URL
            other_href = gif_to_jpeg("https://pubs.acs.org" + other_gif)

            # set different img path for other gif
            img_path = "img/generated/" + coden + '/' + \
                str(datecode) + "/" + str(cleanDOI) + fig_id + ".jpeg"

            # set desired download path  name for other gif
            pathEnding = coden + '/' + str(datecode) + '/'
            filename = "app/static/img/generated/" + pathEnding + cleanDOI + fig_id + '.jpeg'
            # create folder on local computer for images if doesn't exist already
            create_img_folder(pathEnding)
            try:
                download_toc_image(filename, other_href, coden, datecode, cleanDOI)
            except:
                pass
        else:
            # desired file name
            pathEnding = coden + '/' + str(datecode) + '/'
            filename = "app/static/img/generated/" + pathEnding + cleanDOI + '.jpeg'
            # create folder on local computer for images if doesn't exist already
            create_img_folder(pathEnding)
            try:
                download_toc_image(filename, toc_href, coden, datecode, cleanDOI)
            except:
                pass


        articleinfo = {
            "DOI": DOI,
            "Title": html_title,
            "article-link": article_link,
            "Authors": str(authors_joined),
            "toc_href": str(toc_href),
            "other_href": str(other_href),
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





    print results

    return results
