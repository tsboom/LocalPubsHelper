'''
download mp3s from list of image href

'''
import urllib


def downloadTOC(href_list):
    # download image into that directory
    urlfilenamepair = zip(href_list, clean_journal)
    for href, y in urlfilenamepair:
        filename = y + ".jpeg"
        urllib.urlretrieve(href, filename)
