global coden

def lookUpCoden(DOI):
    cleanDOI = DOI.replace("10.1021/", "").replace(".", "")
    journalprefix = cleanDOI[:-7]
    clean_journal.append(cleanDOI)
    coden = constants.CODEN_MATCH[journalprefix]
    return coden;


def getTitle(DOI):


def getTocImage(DOI):

def getAuthors(DOI):

def getCitationYear(DOI):

def getCitationVolume(DOI):

def getCitationIssue(DOI):

def downloadTocImage(DOI):
