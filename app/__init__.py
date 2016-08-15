from flask import Flask, render_template, request, json, jsonify. redirect, url_for
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__, static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views
