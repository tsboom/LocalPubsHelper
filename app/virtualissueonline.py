from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pdb
import urllib
from pprint import pprint
import csv
import os, sys
import shutil
import zipfile
import errno


#debugging
#import pdb #use pdb.set_trace() to break


def createVI(myDOIs):

    global results

    #get current YYYYMMDD
    import datetime
    date = datetime.date.today()
    datecode = datetime.datetime.now().strftime("%Y%m%d")


    #dictionary to match stripped dois with their corresponding coden (for URL formation)
    coden_match = {
        'ar': 'achre4',
        'jf': 'jafcau',
        'ac': 'ancham',
        'am': 'aamick',
        'bi': 'bichaw',
        'bc': 'bcches',
        'bm': 'bomaf6',
        'ab': 'abseba',
        'cs': 'accacs',
        'oc': 'acscii',
        'cb': 'acbcct',
        'ed': 'jceda8',
        'je': 'jceaax',
        'ci': 'jcisd8',
        'cn': 'acncdm',
        'tx': 'crtoec',
        'cr': 'chreay',
        'ct': 'jctcce',
        'cm': 'cmatex',
        'co': 'acsccc',
        'cg': 'cgdefu',
        'ef': 'enfuem',
        'es': 'esthag',
        'ez': 'esthag',
        'ie': 'iecred',
        'id': 'aidcbc',
        'ic': 'inocaj',
        'ja': 'jacsat',
        'la': 'langd5',
        'mz': 'amlccd',
        'ma': 'mamobx',
        'jm': 'jmcmar',
        'ml': 'amclct',
        'mp': 'mpohbp',
        'nn': 'ancac3',
        'nl': 'nalefd',
        'np': 'jnprdf',
        'jo': 'joceah',
        'ol': 'orlef7',
        'op': 'oprdfk',
        'om': 'orgnd7',
        'ph': 'apchd5',
        'jp': 'jpcafh',
        'jpb': 'jpcbfk',
        'jpc': 'jpccck',
        'jz': 'jpclcd',
        'pr': 'jprobs',
        'se': 'ascefj',
        'sc': 'ascecg',
        'sb': 'asbcd6',
        'acsaccounts': 'achre4',
        'acsjafc': 'jafcau',
        'acsanalchem': 'ancham',
        'acsami': 'aamick',
        'acsbiochem': 'bichaw',
        'acsbioconjchem': 'bcches',
        'acsbiomac': 'bomaf6',
        'acscatal': 'accacs',
        'acscentsci': 'acscii',
        'acschembio': 'acbcct',
        'acsjchemed': 'jceda8',
        'acsjced': 'jceaax',
        'acsjcim': 'jcisd8',
        'acschemneuro': 'acncdm',
        'acschemrestox': 'crtoec',
        'acschemrev': 'chreay',
        'acsjctc': 'jctcce',
        'acschemmater': 'cmatex',
        'acscombsci': 'acsccc',
        'acscgd': 'cgdefu',
        'acsenergyfuels': 'enfuem',
        'acsest': 'esthag',
        'acsestlett': 'estlcu',
        'acsiecr': 'iecred',
        'acsinfecdis': 'aidcbc',
        'acsinorgchem': 'inocaj',
        'jacs': 'jacsat',
        'acslangmuir': 'langd5',
        'acsmacrolett': 'amlccd',
        'acsmacromol': 'mamobx',
        'acsjmedchem': 'jmcmar',
        'acsmedchemlett': 'amclct',
        'acsmolpharmaceut': 'mpohbp',
        'acsnano': 'ancac3',
        'acsnanolett': 'nalefd',
        'acsjnatprod': 'jnprdf',
        'acsjoc': 'joceah',
        'acsorglett': 'orlef7',
        'acsoprd': 'oprdfk',
        'acsorganomet': 'orgnd7',
        'acsomega': 'acsodf',
        'acsphotonics': 'apchd5',
        'acsjpca': 'jpcafh',
        'acsjpcb': 'jpcbfk',
        'acsjpcc': 'jpccck',
        'acsjpclett': 'jpclcd',
        'acsjproteome': 'jprobs',
        'acssensors': 'ascefj',
        'acssuschemeng': 'ascecg',
        'acssynbio': 'asbcd6'
    }


    #format results
    results = []


    AUTHOR_XPATH = ("//span[@class=\"hlFld-ContribAuthor\"]/span[@class=\"hlFld-ContribAuthor\"]/a | " + 
    "//*[@id=\"authors\"]/span/span/span/x | //*[@id=\"authors\"]/span/span/a[@href='#cor1'] | //*[@id=\"authors\"]/span/span/a[@href='#cor2'] | //*[@id=\"authors\"]/span/span/a[@href='#cor3']")
    
    '''
    Loop through the DOIS to find information from each article page. add that info to lists. 

    '''
    clean_journal = []



    for DOI in myDOIs:

        DOI = DOI.strip()


        #collect journal prefixes
        
        cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
        journalprefix = cleanDOI[:-7]
        clean_journal.append(cleanDOI)

        coden = coden_match[journalprefix]

        #create image URL for PB using coden and today's date. 
        img_url = ("/pb-assets/images/selects/" + str(coden) + "/" + str(datecode) + "/" + str(cleanDOI) + ".jpeg")

        #create article URL
        article_link = ("/doi/abs/" + str(DOI))

        #open selenium window
        # driver = webdriver.PhantomJS(service_log_path='/home/deploy/pubshelper/ghostdriver.log', executable_path="/home/deploy/pubshelper/phantomjs")
        # driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
        # driver = webdriver.PhantomJS()
        driver = webdriver.PhantomJS()
        driver.set_window_size(1120,550)
        

        #go to full article page by adding URL prefix to DOI
        driver.get("http://pubs.acs.org/doi/full/" + DOI)

        #wait ten seconds and get title text to add to results object
        title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "hlFld-Title")))
        html_title = title.get_attribute('innerHTML').encode('utf-8')
        

        # add title to list of titles (with special characters)
        # article_titles.append(title.get_attribute('innerHTML').encode('utf-8'))
        
       

        # get authors
        authors = driver.find_elements_by_xpath(AUTHOR_XPATH)

        #join the text in the array of the correctly encoded authors
        authors_scrape = []
        for author in authors:
            authors_scrape.append(author.text.encode('utf-8'))
        
        #deal with 2 and more authors formatting
        if ',' not in authors_scrape:
            authors_scrape = [x.replace('and', ' and ') for x in authors_scrape]
        else: 
            authors_scrape = [x.replace(',', ', ').replace(' and', 'and ') for x in authors_scrape]
        
        authorsjoined = (''.join(authors_scrape))

        # #Get citation info
        # CITATION_XPATH = "//*[@id=\"citation\"]"
        # journalcite = driver.find_elements_by_xpath(CITATION_XPATH)

        # citationprep = []
        # for part in journalcite:
        #     citationprep.append(part.text.encode('utf-8'))

        # fullcitation = (''.join(citationprep))

        #Get abbreviated Journal name
        JOURNAL_XPATH = "//*[@id=\"citation\"]/cite"
        journalscrape = driver.find_elements_by_xpath(JOURNAL_XPATH)
        
        for i in journalscrape:
            journal = i.text.encode('utf-8')

        

        #set up soup for BS4

        citationtag = driver.find_element_by_id("citation")
        outcitationtag = citationtag.get_attribute("outerHTML")
        soup = BeautifulSoup(outcitationtag, "html.parser")

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
        

        #Get citation voume or set to empty string  

        try:
            volume = soup.find("span", class_="citation_volume").text
            if volume is None:
                raise Exception
            else:
                volume = volume.encode("utf-8")
            
        except:
            volume = ''
            print 'volume not found'

        # Get issue info or set to empty string

        try:
            issue_info = soup.find("span", class_="citation_volume").next_sibling
            if issue_info is None:
                raise Exception
            issue_info = issue_info.encode("utf-8")
            
        except:
            issue_info = ''
            print 'issue not found'

        
        #click figures link and form url, or set to empty string
        try:
            driver.find_element_by_class_name('showFiguresLink').click()
            
            #get toc image href
            img_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
            if img_box is None:
                raise Exception
            toc_href = img_box.find_element_by_css_selector('a').get_attribute('href')
        except:
            toc_href = ''
            print 'no figures found'

        
        
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
            "Clean_doi": cleanDOI
        }
        

        driver.close()
        driver.quit()
        print "\n"  
        print articleinfo;
        print "\n"


        results.append(articleinfo)

    # print results
    print results

    #write python dict to a csv file
    keys = results[0].keys()

    with open('vi-csv.csv', 'wb') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)



    '''
    check to see if there is an existing folder for coden and date, if not, create the folder

    '''
    #create folder for journal coden and date stamp
    try:
        os.makedirs("app/static/img/virtualissue/"+ coden + '/' + str(datecode)+ "/")
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
        pass

    
        

    '''
    download images from list of image href

    '''


    for articleinfo in results:
        filename = "app/static/img/virtualissue/" + coden + '/' + str(datecode) + "/" + articleinfo["Clean_doi"] + '.jpeg'
        href = articleinfo["toc_href"]
        

        urllib.urlretrieve(href, filename)


    '''
    ZIP images using shutil
    
    '''
    output_filename = 'test'
    filedirectory = "app/static/img/virtualissue/" + coden + '/' + str(datecode) + "/"

    shutil.make_archive(datecode, 'zip', filedirectory)
    shutil.copy(datecode + '.zip', filedirectory)

