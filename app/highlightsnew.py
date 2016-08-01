#! python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from constants import AUTHOR_XPATH, CODEN_MATCH
import pdb
import urllib
import errno
import os, sys
import shutil
import zipfile


#debugging
#import pdb #use pdb.set_trace() to break


def processDOI(myDOIs):

    global imgurls
    global articlelink
    global articletitles
    global authorslist
    global results
    global coden
    global datecode

    '''

    dealing with creating custom URLS for each DOI

    '''
    #Steps to prepare....

    #get current YYYYMMDD
    import datetime
    date = datetime.date.today()
    datecode = datetime.datetime.now().strftime("%Y%m%d")



    # create list of urls with stripped dois, and list of stripped dois 
    clean_journal = []
    clean_doi_list = []

    for y in myDOIs:
        y = y.strip()
        clean_doi_list.append(y)
        y = y.replace("10.1021/","").replace(".","")
        clean_journal.append(y)

    


    #Cross-check stripped doi with journal coden dictionary, and use the coden.
        #remove journal IDs from clean_journal to keep just the cleaned journal name

    journal_name = []

    for d in clean_journal:
        d = d[:-7]
        journal_name.append(d)

    
    # convert list of shortened journal names into new list of corresponding codens
    converted_journal = []
    for n in journal_name:
        coden = CODEN_MATCH[n]
        converted_journal.append(coden)


    #create abcd.jpeg for each article
    jpeg_path = []
    for coden, y in zip(converted_journal, clean_journal):
        y = y + ".jpeg"
        path = 'img/' + coden + '/' + datecode + "/" + y
        jpeg_path.append(path)



    
    
    '''
    Loop through the DOIS to find information from each article page. add that info to lists. 

    '''



    #instantiate the lists that the process will populate
        
    articletitles = []
    href_list = [] 
    articlelink = []
    authorslist = []
    
    # driver = webdriver.PhantomJS(service_log_path='/home/deploy/pubshelper/ghostdriver.log', executable_path="/home/deploy/pubshelper/phantomjs")
    driver = webdriver.PhantomJS()

    driver.set_window_size(1120,550)

    for i in myDOIs:

        #go to full article page by adding URL prefix to DOI

        driver.get("http://pubs.acs.org/doi/full/" + i)

        #wait ten seconds and get title text
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hlFld-Title")))


        # add title to list of titles (with special characters)
        articletitles.append(title.get_attribute('innerHTML'))
        
        # create article URLS for PB, add to list
        articlelink.append("/doi/abs/" + str(i) + "\n")

        # get authors
        authors = driver.find_elements_by_xpath(AUTHOR_XPATH)

        #join the text in the array of the correctly encoded authors
        authors_scrape = []
        for author in authors:
            authors_scrape.append(author.text.encode('utf-8'))
           
        authors_scrape = [re.sub(r"\Aand\b", ' and ', item) for item in authors_scrape]
        authors_scrape = [re.sub(r"\A,$", ', ', item) for item in authors_scrape]
        authors_scrape = [item.replace(', and', ', and ') for item in authors_scrape]


        #deal with 2 and more authors formatting
        # if ',' not in authors_scrape:
        #     authors_scrape = [x.replace('and', ' and ') for x in authors_scrape]
        # else: 
        #     authors_scrape = [x.replace(',', ', ').replace(' and', 'and ') for x in authors_scrape]
        
        authorsjoined = (''.join(authors_scrape))

        authorslist.append(authorsjoined)



        #click figures link and form hi-res image url, or get low quality toc_image
        try:
            driver.find_element_by_class_name('showFiguresLink').click()
            
            #get toc image href
            img_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
            if img_box is None:
                raise Exception
            toc_href = img_box.find_element_by_css_selector('a').get_attribute('href')
        except:
            toc_image = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CLASS_NAME, "figBox"))
            toc_href = toc_image.find_element_by_css_selector('img').get_attribute('src')
            print 'no hi-res figure found'
        # add toc_href to list of URLS to download later and rename according to the DOI
        href_list.append(toc_href)
        
     

        # open a new tab and repeat
        driver.implicitly_wait(8) # seconds
        driver.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 't')


    driver.close()
    driver.quit()
    


    #form img prefix according to checked coden
    imgurls = []
    img_filenames = []
    for coden, journal in zip(converted_journal, clean_journal):
        img_prefix = ("/pb-assets/images/" + str(coden) + "/highlights/" + str(datecode) + 
        "/" + str(journal) + ".jpeg")
        img_filename = str(journal + ".jpeg")
        img_filenames.append(img_filename)
        imgurls.append(img_prefix)
    

    


    '''
    download mp3s from list of image href

    '''
    #create folder for journal coden and date stamp
    try:
        os.makedirs("app/static/img/"+ coden + '/' + str(datecode)+ "/")
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
        pass

    urlfilenamepair = zip(href_list, clean_journal)
    filedirectory = "app/static/img/" + coden + '/' + str(datecode) + "/"


    for href, y in urlfilenamepair:
            filename =  filedirectory + y + ".jpeg"
            urllib.urlretrieve(href, filename)
            

    '''
    ZIP images using shutil
    
    '''
    output_filename = 'test'

    shutil.make_archive(datecode, 'zip', filedirectory)
    shutil.move(datecode + '.zip', filedirectory)



    #combine results lists into one list

        
    results = zip(articlelink, imgurls, articletitles, authorslist, jpeg_path)   
    return results, coden, datecode
    




   




   










