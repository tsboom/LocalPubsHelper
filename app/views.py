from app import app, render_template, request, json
from celery import celery

import highlightsnew

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signUp')
def submit():
    return render_template('signUp.html')
    
@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password}); 
    return render_template('results.html')


# @app.route('highlights', methods=['POST'])
# def highlights():
#     doiList = request.form["pasteddois"]
#     with doiLIST as infile:
#         myDOIs = [line.strip() for line in infile]
#     # run python process
#     result = processDOI(myDOIs)
#     return render_template('results.html')

if __name__ == '__main__':
    app.run()