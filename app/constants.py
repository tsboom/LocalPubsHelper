
# constants


# constants to help format URL strings

DOI_PREFIX = "http://pubs.acs.org/doi/"






#dictionary to match stripped dois with their corresponding coden (for URL formation)

CODEN_MATCH = {
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
    'acsbiomaterials': 'abseba',
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
    'acsearthspacechem': 'aesccq',
    'acsenergyfuels': 'enfuem',
    'acsenergylett': 'aelccp',
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
    'acssynbio': 'asbcd6',
    'acssensors': 'ascefj',
    'acsaem': 'aaemcq',
    'acsanm': 'aanmf6',
    'aabmcb': 'aabmcb',
    'aptsfn': 'aptsfn'
}



AUTHOR_XPATH = ("//span[@class=\"hlFld-ContribAuthor\"]/span[@class=\"hlFld-ContribAuthor\"]/a | " +
    # "//*[@id=\"authors\"]/span/span/span/x | " +
    " //*[@id=\"authors\"]/span/span/a[@href='#cor1'] | " +
    " //*[@id=\"authors\"]/span/span/a[@href='#cor2'] | "+
    "//*[@id=\"authors\"]/span/span/a[@href='#cor3']")
