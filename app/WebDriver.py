#! python2.7
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

class WebDriver:
    def __init__(self, DOI):
        self.DOI = DOI
        self.title = ""
        self.authors_list = []
        self.toc_image_url = ""
        self.alt_image_url = ""
        self.coden = ""
        self.citation = []


    def lookUpCoden(DOI):
        cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
        journalprefix = cleanDOI[:-7]
        clean_journal.append(cleanDOI)
        self.coden = constants.CODEN_MATCH[journalprefix]


    def getTitle(DOI):


    def getTocImage(DOI):

    def getAuthors(DOI):

    def getCitationYear(DOI):

    def getCitationVolume(DOI):

    def getCitationIssue(DOI):

    def downloadTocImage(DOI):
