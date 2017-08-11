from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
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


        # get picture link
        gif_url = "https://pubs.acs.org" + article.toc_gif

        toc_href = gif_to_jpeg(gif_url)




        # Get abbreviated Journal name
        print "getting journal name"
        JOURNAL_XPATH = "//*[@id=\"citation\"]/cite"
        journalscrape = driver.find_elements_by_xpath(JOURNAL_XPATH)

        for i in journalscrape:
            journal = i.text.encode('utf-8')

        print "\t" + journal
        # set up soup for BS4

        citationtag = driver.find_element_by_id("citation")
        outcitationtag = citationtag.get_attribute("outerHTML")
        soup = BeautifulSoup(outcitationtag, "html.parser")

        print "getting year"
        # set year to citation year or empty string
        try:
            year = soup.find("span", class_="citation_year").text
            if year is None:
                raise Exception
            else:
                year = year.encode("utf-8")

        except:
            year = ''
            print 'year not found'

        print "\t" + year
        # Get citation voume or set to empty string
        print "getting issue"
        try:
            volume = soup.find("span", class_="citation_volume").text
            if volume is None:
                raise Exception
            else:
                volume = volume.encode("utf-8")

        except:
            volume = ''
            print 'volume not found'
        print "\t" + volume
        # Get issue info or set to empty string
        print "getting issue info"
        try:
            issue_info = soup.find(
                "span", class_="citation_volume").next_sibling
            if issue_info is None:
                raise Exception
            issue_info = issue_info.encode("utf-8")

        except:
            issue_info = ''
            print 'issue not found'
        print "\t" + issue_info
        # click figures link and form url, or set to empty string
        print "getting figures link"
        try:
            driver.find_element_by_class_name('showFiguresLink').click()

            # get toc image href
            img_box = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
            if img_box is None:
                raise Exception
            toc_href = img_box.find_element_by_css_selector(
                'a').get_attribute('href')

        except:
            # toc_image = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "figBox")))
            # toc_href = toc_image.find_element_by_css_selector('img').get_attribute('src')
            toc_href = ""
            print 'no hi-res figure found'
        print "\t" + toc_href

        articleinfo = {
            'DOI': DOI,
            'Title': html_title,
            'article-link': article_link,
            'Authors': str(authorsjoined),
            'toc_href': str(toc_href),
            'Image': img_url,
            # "full-citation": fullcitation
            'Journal': journal,
            'Volume': volume,
            'Issue-info': issue_info,
            'Year': year,
            "Datecode": datecode,
            "Clean_doi": cleanDOI,
            'Coden': coden
            }


        driver.close()
        driver.quit()

        results.append(articleinfo)



    # write python dict to a csv file
    keys = results[0].keys()

    with open('app/vi-csv.csv', 'wb') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

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

    '''
    download images from list of image href

    '''

    for articleinfo in results:
        try:
            filename = "app/static/img/generated/virtualissue/" + coden + '/' + \
            str(datecode) + "/" + articleinfo["Clean_doi"] + '.jpeg'
        except:
            pass
        try:
            href = articleinfo["toc_href"]
        except:
            pass

        try:
            urllib.urlretrieve(href, filename)
        except IOError:
            print "No image found for " + DOI
            pass

    '''
    ZIP images using shutil

    '''
    filedirectory = "app/static/img/generated/virtualissue/" + \
        coden + '/' + str(datecode) + "/"

    shutil.make_archive(datecode, 'zip', filedirectory)
    shutil.copy(datecode + '.zip', filedirectory)

    return results
