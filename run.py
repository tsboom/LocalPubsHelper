#!flask/bin/python

# python run.py in dir to start local server

from app import app

app.run(debug=True, host='0.0.0.0', port=8080)