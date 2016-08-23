
from flask import Flask, render_template, request, json, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename



__author__ = "tsboom"




# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
#
# ALLOWED_EXTENSIONS = set(['csv'])
#
# <<<<<<< HEAD
# app = Flask(__name__, static_url_path='')
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# =======
app = Flask(__name__, static_url_path='/static')



from app import views
