from flask import Flask, render_template, request, json, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

ALLOWED_EXTENSIONS = set(['csv'])

<<<<<<< HEAD
app = Flask(__name__, static_url_path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

=======
app = Flask(__name__, static_url_path='/static')
>>>>>>> e45b448c784b8a5b8ac1b5ec33bab07f7b345026

from app import views
