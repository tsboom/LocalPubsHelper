
# -*- coding: utf-8 -*-
from app import app, render_template, request, json
import csv
import pdb
import string
from table_fu import TableFu

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#import pdb #use pdb.set_trace() to break

from highlightsnew import processDOI
from virtualissue import viScrapingForDOI
# import virtualissue

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/virtualissue')
def virtualissue():
    return render_template('virtualissue.html')

    
@app.route('/virtualissueprocess', methods=['POST'])
def virtualissueautomate():
    global viDOIs
    viDOIs = str(request.form["text"]).split('\r\n')
    
    for DOI in viDOIs:
        viScrapingForDOI(DOI)
    pdb.set_trace() 

    return render_template('virtualissueresults.html', results = results)



@app.route('/submit-form', methods=['POST'])
def highlights():
    #get text from textarea, split it up DOIS into a list
    doiLIST = str(request.form['text'])

    global myDOIs
    myDOIs = doiLIST.split('\r\n')
    
    # run python process
    results = processDOI(myDOIs)
    
    return render_template('results.html', results=results, resultsarray = results)

@app.route('/csv')
def langmuir():
    return render_template('csvindex.html')


@app.route('/csvprocess', methods =['POST'])
def langmuirresult():
    global table
    # data = request.form['text']
    table = TableFu.from_file('app/data.csv')
    return render_template('vi-template.html', table=table)

if __name__ == '__main__':
    app.run()