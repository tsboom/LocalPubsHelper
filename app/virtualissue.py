from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import pdb
import urllib
from pprint import pprint



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





AUTHOR_XPATH = "//span[@class=\"hlFld-ContribAuthor\"]/span[@class=\"hlFld-ContribAuthor\"]/a | //*[@id=\"authors\"]/span/span/span/x | //*[@id=\"authors\"]/span/span/a/sup"

'''
Loop through the DOIS to find information from each article page. add that info to lists. 

'''

DOI = "10.1021/acscatal.5b01667"

def viScrapingForDOI(DOI):

    cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
    journalprefix = cleanDOI[:-7]

    coden = coden_match[journalprefix]

    #create image URL for PB using coden and today's date. 
    img_url = ("/pb-assets/images/selects/" + str(coden) + "/" + str(datecode) + "/" + str(cleanDOI) + ".jpeg")

    #create article URL
    article_link = ("/doi/abs/" + str(DOI))

    #open selenium window
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120,550)
    

    #go to full article page by adding URL prefix to DOI
    driver.get("http://pubs.acs.org/doi/full/" + DOI)

    #wait ten seconds and get title text to add to results object
    title = WebDriverWait(driver, 13).until(EC.presence_of_element_located((By.CLASS_NAME, "hlFld-Title")))


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
    
    #authors_list.append(authorsjoined)


    
    #click figures link
    driver.find_element_by_class_name('showFiguresLink').click()
    #get toc image href
    img_box = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "highRes")))
    toc_href = img_box.find_element_by_css_selector('a').get_attribute('href')


    articleinfo = {
        "doi": DOI,
        "article-title": title.get_attribute('innerHTML').encode('utf-8'),
        "article-link": article_link,
        "authors": authorsjoined.encode('utf-8'),
        "toc_href": str(toc_href),
        "img-url": img_url,
        # "journal": ,
        # "volume": ,
        # "issue-info": ,
        # "citation-year": ,
    }


    driver.close()
    driver.quit()
      
    return articleinfo;


#get dois from txt file

with open('doi_list.txt', 'r') as infile:
          myDOIs = [line.strip() for line in infile]


#format results
results = {
    "articles":[
        

    ]
}


for DOI in myDOIs:
    #call function
    results.update(articleinfo)

print results





    # #print dois (minus periods), image url (using clean doi), title html, and TOC image link in nice way. 

    # for (a, b, c, d) in zip(img_urls, article_link, article_titles, authors_list):
    #     print a + "\n", b + "\n", c + "\n", d + "\n" + "\n----\n"

    

    # '''
    # download mp3s from list of image href

    # '''

    # #download image into that directory
    # urlfilenamepair = zip(href_list, clean_journal)
    # for href, y in urlfilenamepair:
    #         filename =  y + ".jpeg"
    #         urllib.urlretrieve(href, filename)

