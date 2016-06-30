from flask import Flask, render_template, request, json, jsonify

app = Flask(__name__, static_url_path='')



from app import views