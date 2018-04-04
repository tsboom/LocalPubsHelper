
# -*- coding: utf-8 -*-
from app import app, render_template, request, jsonify, redirect, url_for
import csv
import pdb
import string
import constants
from table_fu import TableFu
from werkzeug.utils import secure_filename
from highlightsnewtest import processDOI
from virtualissueASAP import createVI
from pymongo import MongoClient
import os
import sys
import datetime
import json
from bson import json_util


reload(sys)
sys.setdefaultencoding('utf-8')

# import pdb #use pdb.set_trace() to break
"""
database stuff.
make sure mongo daemon is started in a terminal window (type mongod)
"""
client = MongoClient('localhost', 27017)

db = client.pubshelper

#create a collection within the database called highlights
highlights = db.highlights

#create a collection within the db called virtualissues
virtualissues = db.virtualissues



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/submit-form', methods=['POST'])
def highlights():


    # get text from textarea, split it up DOIS into a list
    doiLIST = str(request.form['text'])

    global myDOIs
    myDOIs = doiLIST.split('\r\n')

    # run python process
    results = processDOI(myDOIs)

    #save results to db
    saved_results = db.highlights.insert_one({"data": results, "datetime": datetime.datetime.utcnow() })

    return render_template('results.html', results=results)

# virtual issue index and virtual issue process results


@app.route('/doivirtualissue')
def virtualissue():
    return render_template('virtualissue.html')


@app.route('/doivirtualissueprocess', methods=['POST'])
def virtualissueautomate():

    # get checkbox
    multiJournal = request.form.get('checkbox', default=False, type=bool)

    # get tracking code
    trackingCode = request.form["vi-tracking"]

    # get vi-short-name
    shortName = request.form['vi-short-name']

    # get DOIs
    myDOIs = str(request.form["DOIs"]).split('\r\n')

    # run python process
    results = createVI(myDOIs, multiJournal, trackingCode, shortName)

    #save results to db
    saved_results = db.virtualissues.insert_one({"data": results, "datetime": datetime.datetime.utcnow() })

    return render_template('vi-template.html', results=results)


'''
index for processing a csv into a virtual issue
'''
# set upload folder and allowed extensions

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# check if extension is allowed


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/csv')
def csvvi():
    return render_template('csvindex.html')


@app.route('/csvupload', methods=['POST'])
def csvviresult():
    if request.method == 'POST':
    # Get the name of uploaded file
        file = request.files['file']
        # Check if the file is an allowed extension
        if file and allowed_file(file.filename):
            # Make the filename safe - remove unsupported characters
            filename = secure_filename(file.filename)
            # # Move the file from the temp folder to the upload folder
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # Use tablefu to template out the uploaded CSV file
            global table
            table = TableFu.from_file('app/static/uploads/'+ filename)
            return render_template('virtualissueresults.html', table=table)

'''
podcast index and process results

'''


@app.route('/podcast')
def podcast():
    return render_template('podcastindex.html')


@app.route('/podcastupload', methods=['GET', 'POST'])
def podcastupload():
    if request.method == 'POST':
    # Get the name of uploaded file
        file = request.files['file']
        # Check if the file is an allowed extension
        if file and allowed_file(file.filename):
            # Make the filename safe - remove unsupported characters
            filename = secure_filename(file.filename)
            # # Move the file from the temp folder to the upload folder
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # Use tablefu to template out the uploaded CSV file
            global table
            table = TableFu.from_file('app/static/uploads/' + filename)
            return render_template('podcastresults.html', table=table)


'''

API stuff

'''


@app.route('/api/dois', methods=['POST'])
def get_dois():
    #get DOIs from react application input box, insert JSON into mongo??
    return "hello"

@app.route('/api/highlights', methods=['GET'])
def highlights_results():
    #find most recent highlight result
    highlights_results = db.highlights.find().sort("datetime", -1).limit(1)
    data = highlights_results[0]["data"]

    return jsonify({"highlights_results": data})


@app.route('/api/virtualissue', methods=['GET'])
def virtualissue_results():
    #find most recent highlight result
    vi_results = db.virtualissues.find().sort("datetime", -1).limit(1)
    data = vi_results[0]["data"]

    return jsonify({"virtualissue_results": data})

if __name__ == '__main__':
    app.run()
