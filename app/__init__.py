from flask import Flask, render_template, request, json

app = Flask(__name__)
from app import views