from flask import Flask, render_template, request, json, jsonify
from app import views

app = Flask(__name__, static_url_path='/static')
