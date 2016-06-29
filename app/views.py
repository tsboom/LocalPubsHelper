
# -*- coding: utf-8 -*-
from app import app, render_template, request, jsonify
import csv
import pdb
import string
from table_fu import TableFu

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#import pdb #use pdb.set_trace() to break

from highlightsnewtest import processDOI
# from virtualissue import createVI
from virtualissueASAP import createVI
# import virtualissue


#index page starts with box to paste DOIs for highlights
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# virtual issue index and virtual issue process results    
    
@app.route('/doivirtualissue')
def virtualissue():
    return render_template('virtualissue.html')

    
@app.route('/doivirtualissueprocess', methods=['POST'])
def virtualissueautomate():
    
    myDOIs = str(request.form["text"]).split('\r\n')
    
 
     # run python process
    createVI(myDOIs)

    global table
    # data = request.form['text']
    table = TableFu.from_file('vi-csv.csv')
    return render_template('vi-template.html', table=table)


#results of highlights helper
@app.route('/submit-form', methods=['POST'])
def highlights():
    #get text from textarea, split it up DOIS into a list
    doiLIST = str(request.form['text'])

    global myDOIs
    myDOIs = doiLIST.split('\r\n')
    
    # run python process
    results = processDOI(myDOIs)
    
    return render_template('results.html', results=results)

#index for processing a csv into a virtual issue
@app.route('/csv')
def csvvi():
    return render_template('csvindex.html')


@app.route('/csvprocess', methods =['POST'])
def csvviresult():
    global table
    # data = request.form['text']
    # table = TableFu.from_file('app/vi-csv.csv')
    table = TableFu.from_file('app/vi-csv.csv')
    # return render_template('vi-template.html', table=table)
    return render_template('vi-template.html', table=table)

#podcast index and process results
@app.route('/podcast')
def podcast():
    return render_template('podcastindex.html')

@app.route('/podcastprocess', methods=['POST'])
def podcastresult():
    global table
    table = TableFu.from_file('app/chembio.csv')
    return render_template('podcastresultsnano.html', table=table)

# @app.route('/interactive/')
# def interactive():
#     return render_template('interactive.html')


# @app.route('/background_process')
# def background_process():
#     try:
#         lang = request.args.get('proglang', 0, type=str)
#         if lang.lower() == 'python':
#             return jsonify(result='You are wise')
#         else:
#             return jsonify(result='Try again.')
#     except Exception as e:
#         return str(e)


if __name__ == '__main__':
    app.run()