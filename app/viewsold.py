#first attempt at views

from app import app, render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/highlightshelper')
def highlightshelper():
    return render_template('highlightshelper.html')