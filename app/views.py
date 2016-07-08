
# -*- coding: utf-8 -*-
from app import app, render_template, request, jsonify, redirect, url_for
import csv
import pdb
import string
from table_fu import TableFu
import os
from werkzeug.utils import secure_filename

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#import pdb #use pdb.set_trace() to break

from highlightsnewtest import processDOI
# from virtualissue import createVI
from virtualissueASAP import createVI
# import virtualissue



#code that checks if extention is valid, and then uploads the file and redirects the user to the URL for the uploaded file
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


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
    
    myDOIs = str(request.form["text"])
    myDOIs = [doi for doi in myDOIs.split('\r\n') if doi]
 
     # run python process
    results = createVI(myDOIs)

    global table
    # data = request.form['text']
    table = TableFu.from_file('app/vi-csv.csv')
    return render_template('vi-template.html', results=results, table=table)


#results of highlights helper
@app.route('/submit-form', methods=['POST'])
def highlights():
    #get text from textarea, split it up DOIS into a list
    doiLIST = str(request.form['text'])

    global myDOIs
    myDOIs = str(request.form["text"])
    myDOIs = [doi for doi in myDOIs.split('\r\n') if doi]
    
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
    table = TableFu.from_file('app/ancham-may.csv')
    return render_template('podcastresultsancham.html', table=table)

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