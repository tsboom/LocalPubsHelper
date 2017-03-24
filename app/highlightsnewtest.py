#! python2.7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pdb
import urllib
import errno
import os
import sys
import shutil
import zipfile
import constants
import re

# debugging
# import pdb #use pdb.set_trace() to break


def processDOI(myDOIs):

    global imgurls
    global articlelink
    global articletitles
    global authorslist
    global results

    '''

    dealing with creating custom URLS for each DOI

    '''
    # Steps to prepare....

    # create empty array to hold results dicts
    results = []

    # get current YYYYMMDD
    import datetime
    date = datetime.date.today()
    datecode = datetime.datetime.now().strftime("%Y%m%d")

    # create list of urls with stripped dois, and list of stripped dois
    clean_journal = []
    clean_doi_list = []

    '''
    Loop through DOIS and find info about each article. add that information to a python dictionary

    '''
    # remove empty strings from list
    myDOIs = [doi for doi in myDOIs if doi]

    for DOI in myDOIs:

        DOI = DOI.strip()

        # collect journal prefixes

        cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
        journalprefix = cleanDOI[:-7]

        coden = constants.CODEN_MATCH[journalprefix]

        # create image URL for PB using coden and today's date.
        img_url = ("/pb-assets/images/" + str(coden) + "/" +
                   "highlights/" + str(datecode) + "/" + str(cleanDOI) + ".jpeg")

        # create article URL
        article_link = ("/doi/abs/" + str(DOI))

        # create img path for Flask, so that the images can be displayed on
        # Flask.
        img_path = "img/generated/" + coden + '/' + \
            str(datecode) + "/" + str(cleanDOI) + ".jpeg"

        # Open Phantom JS

        # driver = webdriver.PhantomJS(service_log_path='/home/deploy/pubshelper/ghostdriver.log', executable_path="/home/deploy/pubshelper/phantomjs")
        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)

        # go to full article page by adding URL prefix to DOI
        driver.get("http://pubs.acs.org/doi/full/" + DOI)

        # wait ten seconds and get title text to add to results object
        title = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "hlFld-Title")))
        html_title = title.get_attribute('innerHTML').encode('utf-8')

        # get authors
        authors = driver.find_elements_by_xpath(constants.AUTHOR_XPATH)

        # join the text in the array of the correctly encoded authors
        authors_scrape = []
        for author in authors:
            authors_scrape.append(author.text.encode('utf-8'))



        # create array to hold formatted authors list (stars next to authors)
        authorsStars = []

        # iterate over authors_scrape and join * with author before it
        for index, i in enumerate(authors_scrape):
            if index != (len(authors_scrape)-1):
                if authors_scrape[index+1] == "*":
                    string = authors_scrape[index] + authors_scrape[index+1]
                    del(authors_scrape[index+1])
                    # add string
                    authorsStars.append(string)
                else:
                    authorsStars.append(authors_scrape[index])
            else:
                authorsStars.append(authors_scrape[index])

        # join correctly formatted authors
        # add ', ' and 'and'
        if len(authorsStars)==2:
            authorsStars.insert(1, ' and ')
            authorsjoined = (''.join(authorsStars))
        elif len(authorsStars)==1:
            authorsjoined = (''.join(authorsStars))
        else:
            all_but_last = ', '.join(authorsStars[:-1])
            last = authorsStars[-1]
            authorsjoined = ', and '.join([all_but_last, last])


        # click figures link and form url, or set to empty string
        try:
            driver.find_element_by_class_name('showFiguresLink').click()

            # get toc image href
            img_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
            if img_box is None:
                raise Exception
            toc_href = img_box.find_element_by_css_selector(
                'a').get_attribute('href')
        except:
            # toc_image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "figBox")))
            # toc_href = toc_image.find_element_by_css_selector('img').get_attribute('src')
            print 'no hi-res figure found'
            toc_href = ""

        articleinfo = {
            "DOI": DOI,
            "Title": html_title,
            "article-link": article_link,
            "Authors": str(authorsjoined),
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

    print results

    driver.close()
    driver.quit()

    '''
    check to see if there is an existing folder for coden and date, if not, create the folder

    '''
    # create folder for journal coden and date stamp
    try:
        os.makedirs("app/static/img/generated/" + coden + '/' + str(datecode) + "/")
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
        pass

    '''
    download images from list of image href

    '''

    for articleinfo in results:
        filename = "app/static/img/generated/" + coden + '/' + \
            str(datecode) + "/" + articleinfo["Clean_doi"] + '.jpeg'
        href = articleinfo["toc_href"]
        try:
            urllib.urlretrieve(href, filename)
        except IOError:
            print "No image found for " + DOI
            pass

    # for href, y in urlfilenamepair:
    #         filename = y + ".jpeg"
    #         urllib.urlretrieve(href, filename)

    '''
    ZIP images using shutil

    '''

    # filedirectory = "app/static/img/generated/" + coden + '/'
    #
    # shutil.make_archive(datecode, 'zip', filedirectory)
    # shutil.copy(datecode + '.zip', filedirectory)

    return results
