class Article:
    "Class that describes an individual ACS article"

    def __init__(self, DOI):
        self.DOI = DOI

    def lookUpCoden(self):
        cleanDOI = self.DOI.replace("10.1021/", "").replace(".", "")
        journalprefix = cleanDOI[:-7]
        coden = constants.CODEN_MATCH[journalprefix]
        return coden

    def getTitle(self):


    def getTocImage(self):

    def getAuthors(self):

    def getCitationYear(self):

    def getCitationVolume(self):

    def getCitationIssue(self):

    def downloadTocImage(self):
