from flask import Flask, render_template, request, json, jsonify
from flask_bootstrap import Bootstrap

app = Flask(__name__)



from app import views