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

    '''

    dealing with creating custom URLS for each DOI

    '''
    #Steps to prepare....

    #create empty array to hold results dicts
    results = []
   
   


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
        'acsenergylett': 'aelccp',
        'acsacsiecr': 'iecred',
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


    AUTHOR_XPATH = ("//span[@class=\"hlFld-ContribAuthor\"]/span[@class=\"hlFld-ContribAuthor\"]/a | " + 
    "//*[@id=\"authors\"]/span/span/span/x | //*[@id=\"authors\"]/span/span/a[@href='#cor1'] | //*[@id=\"authors\"]/span/span/a[@href='#cor2'] | //*[@id=\"authors\"]/span/span/a[@href='#cor3']")
        

    # create list of urls with stripped dois, and list of stripped dois 
    clean_journal = []
    clean_doi_list = []

    '''
    Loop through DOIS and find info about each article. add that information to a python dictionary

    '''

    for DOI in myDOIs:

        DOI = DOI.strip()

        #collect journal prefixes
        cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
        journalprefix = cleanDOI[:-7]

        coden = coden_match[journalprefix]
        
        
       
        #create image URL for PB using coden and today's date. 
        img_url = ("/pb-assets/images/" + str(coden) + "/" + "highlights/" + str(datecode) + "/" + str(cleanDOI) + ".jpeg")

        #create article URL
        article_link = ("/doi/abs/" + str(DOI))

        #create img path for Flask, so that the images can be displayed on Flask. 
        img_path = "img/" + coden + '/' + str(datecode) + "/" + str(cleanDOI) + ".jpeg"


        #Open Phantom JS

        # driver = webdriver.PhantomJS(service_log_path='/home/deploy/pubshelper/ghostdriver.log', executable_path="/home/deploy/pubshelper/phantomjs")
        driver = webdriver.PhantomJS()
        driver.set_window_size(1120,550)

        #go to full article page by adding URL prefix to DOI
        driver.get("http://pubs.acs.org/doi/full/" + DOI)

        #wait ten seconds and get title text to add to results object
        title = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "hlFld-Title")))
        html_title = title.get_attribute('innerHTML').encode('utf-8')  

        # get authors
        authors = driver.find_elements_by_xpath(AUTHOR_XPATH)

        #join the text in the array of the correctly encoded authors
        authors_scrape = []
        for author in authors:
            authors_scrape.append(author.text)
           

        #deal with 2 and more authors formatting
        if ',' not in authors_scrape:
            authors_scrape = [x.replace('and', ' and ') for x in authors_scrape]
        else: 
            authors_scrape = [x.replace(',', ', ').replace(' and', 'and ') for x in authors_scrape]
        
        authorsjoined = (''.join(authors_scrape))

               
        #click figures link and form hi-res image url, or get low quality toc_image
        try:
            driver.find_element_by_class_name('showFiguresLink').click()
            
            #get toc image href
            img_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
            if img_box is None:
                raise Exception
            toc_href = img_box.find_element_by_css_selector('a').get_attribute('href')
        except:
            toc_image = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "absImg")))
            toc_href = toc_image.find_element_by_css_selector('img').get_attribute('src')
            print 'no hi-res figure found for ' + DOI
        
         

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
        print articleinfo;
        print "\n"


        results.append(articleinfo)

    print results

    driver.close()
    driver.quit()
    
    


    '''
    check to see if there is an existing folder for coden and date, if not, create the folder

    '''
    #create folder for journal coden and date stamp
    try:
        os.makedirs("app/static/img/"+ coden + '/' + str(datecode)+ "/")
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise exc
        pass

    '''
    download images from list of image href

    '''


    for articleinfo in results:
        filename = "app/static/img/" + coden + '/' + str(datecode) + "/" + articleinfo["Clean_doi"] + '.jpeg'
        href = articleinfo["toc_href"]
        urllib.urlretrieve(href, filename)


    # for href, y in urlfilenamepair:
    #         filename = y + ".jpeg"
    #         urllib.urlretrieve(href, filename)


            

    '''
    ZIP images using shutil
    
    '''
    output_filename = 'test'
    # filedirectory = "app/static/img/" + coden + '/' + str(datecode) + "/"
    filedirectory = "app/static/img/" + coden + '/' 
    shutil.make_archive(datecode, 'zip', filedirectory)
    shutil.copy(datecode + '.zip', filedirectory)



    return results   
      
    
    




   




   










