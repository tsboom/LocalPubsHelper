from app import app, render_template

import highlightsnew

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/submit')
def submit():
    print "hello world!"
    
    # doiList = request.form["pasteddois"]
    # with doiLIST as infile:
    #     myDOIs = [line.strip() for line in infile]
    # # run python process
    # result = processDOI(myDOIs)



    # return render_template('results.html')

if __name__ == '__main__':
    app.run()