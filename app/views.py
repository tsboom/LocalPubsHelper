
# -*- coding: utf-8 -*-
from app import app, render_template, request, jsonify, redirect, url_for
import csv
import pdb
import string
from table_fu import TableFu
from werkzeug.utils import secure_filename
import os

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# import pdb #use pdb.set_trace() to break

from highlightsnewtest import processDOI
# from virtualissue import createVI
from virtualissueASAP import createVI
# import virtualissue


# index page starts with box to paste DOIs for highlights
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# results of highlights helper

@app.route('/submit-form', methods=['POST'])
def highlights():
    # get text from textarea, split it up DOIS into a list
    doiLIST = str(request.form['text'])

    global myDOIs
    myDOIs = doiLIST.split('\r\n')

    # run python process
    results = processDOI(myDOIs)

    return render_template('results.html', results=results)

# virtual issue index and virtual issue process results


@app.route('/doivirtualissue')
def virtualissue():
    return render_template('virtualissue.html')


@app.route('/doivirtualissueprocess', methods=['POST'])
def virtualissueautomate():

    myDOIs = str(request.form["text"]).split('\r\n')

    # run python process
    results = createVI(myDOIs)

    global table
    # data = request.form['text']
    table = TableFu.from_file('app/vi-csv.csv')
    return render_template('vi-template.html', table=table, results=results)


'''
index for processing a csv into a virtual issue
'''
#set upload folder and allowed extensions

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#check if extension is allowed
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
            table = TableFu.from_file('app/static/uploads/'+ filename)
            return render_template('podcastresults.html', table=table)


if __name__ == '__main__':
    app.run()
