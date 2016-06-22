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


#debugging
#import pdb #use pdb.set_trace() to break


def createVI(myDOIs):


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
    "//*[@id=\"authors\"]/span/span/span/x | //*[@id=\"authors\"]/span/span/a[@href='#cor1']")

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
        title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hlFld-Title")))
        html_title = title.get_attribute('innerHTML').encode('utf-8')
        

        # add title to list of titles (with special characters)
        # article_titles.append(title.get_attribute('innerHTML').encode('utf-8'))
        
      
        # get authors
        authors = driver.find_elements_by_xpath(AUTHOR_XPATH)

        #join the text in the array of the correctly encoded authors
        authors_scrape = []
        for author in authors:
            authors_scrape.append(author.text.encode('utf-8'))
        
        #make sure spacing around authors names is correct     
        if len(authors_scrape) > 2:
            if authors_scrape[1] == 'and':
                authors_scrape[1] = ' and '
                authorsjoined = (''.join(authors_scrape))
            elif authors_scrape[2] == 'and':
                authors_scrape[2] = ' and '
                authorsjoined = (''.join(authors_scrape))
            else: 
                authorsjoined = (''.join(authors_scrape))
                authorsjoined = authorsjoined.replace(',', ', ').replace(' and', 'and ')
        else: 
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

        

        #Get citation year or set to nothing
        year = ''
        try:    
            
            YEAR_XPATH = "//*[@id=\"citation\"]/span[@class=\"citation_year\"]"
            yearscrape = driver.find_elements_by_xpath(YEAR_XPATH)

            for i in yearscrape:
                year = i.text.encode('utf-8')
        except:
            print 'year not found'
            continue

         

        #Get citation volume
        volume = ''
        try:
            
            VOLUME_XPATH = "//*[@id=\"citation\"]/span[@class=\"citation_volume\"]"
            volumescrape = driver.find_elements_by_xpath(VOLUME_XPATH)
            for i in volumescrape:
                volume = i.text.encode('utf-8')
        except:
            print 'volume not found'
            continue

        # Get issue info
        issue_info = ''
        citation = driver.find_element_by_id("citation")
        html = citation.get_attribute("outerHTML")

        soup = BeautifulSoup(html, "html.parser")

        try:
            issue_info = soup.find("span", class_="citation_volume").next_sibling
            issue_info = issue_info.encode("utf-8")
        except:
            print 'issue not found'
            continue

        # somewhere in here teh DOI gets messed up for 10.1021/acs.chemmater.5b01982. 
        print DOI
      
        #click figures link
        toc_href = ''
        try:
            
            driver.find_element_by_class_name('showFiguresLink').click()
        
            #get toc image href
            img_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
            toc_href = img_box.find_element_by_css_selector('a').get_attribute('href')
        except:
            print 'TOC href not found'
            pass

        print DOI

      

        articleinfo = {
            "DOI": DOI,
            "Title": html_title,
            "article-link": article_link,
            "Authors": str(authorsjoined),
            "toc_href": str(toc_href),
            "Image": img_url,
            # "full-citation": fullcitation
            "Journal": journal,
            "Volume": volume,
            "Issue-info": issue_info,
            "Year": year,
        }

        driver.close()
        driver.quit()
        print "\n"  
        print articleinfo;
        print "\n"

        print myDOIs
        results.append(articleinfo)

    # print results

    keys = results[0].keys()

    with open('vi-csv.csv', 'wb') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)




        

    '''
    download mp3s from list of image href

    '''

    # #download image into that directory
    # href_list = []
    # for i in results:
    #     href_list.append(i['toc_href'])

    # urlfilenamepair = zip(href_list, clean_journal)

    # for href, y in urlfilenamepair:
    #         filename =  y + ".jpeg"
    #         urllib.urlretrieve(href, filename)

