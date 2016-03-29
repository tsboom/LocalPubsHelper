from app import app, render_template, request, json
import pdb
#import pdb #use pdb.set_trace() to break

import highlightsnew
# import virtualissue

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
# @app.route('/signUp')
# def submit():
#     return render_template('signUp.html')
    
# @app.route('/signUpUser', methods=['POST'])
# def signUpUser():
#     user =  request.form['username'];
#     password = request.form['password'];
#     return json.dumps({'status':'OK','user':user,'pass':password}); 
#     return render_template('results.html')


@app.route('/submit-form', methods=['POST'])
def highlights():
    pdb.set_trace()
    doiLIST = request.form['text']
    
    
    with doiLIST as infile:
        myDOIs = [line.strip() for line in infile]
    # run python process


    result = processDOI(myDOIs)
    
    return render_template('test.html', result=result, imgurls=imgurls)
#     # return render_template('results.html')
# def virtualissueautomate():
#     doiList = request.form["dois"]
#     lines = [1 for 1 in doiList.split("\n") if 1]

#     for DOI in lines:
#         viScrapingForDOI(DOI)



if __name__ == '__main__':
    app.run()