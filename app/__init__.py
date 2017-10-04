
from flask import Flask, render_template, request, json, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename



__author__ = "tsboom"




app = Flask(__name__, static_url_path='/static')



from app import views
