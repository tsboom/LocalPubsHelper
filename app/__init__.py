from flask import Flask, render_template, request, json, jsonify, redirect, url_for, send_from_directory



__author__ = "tsboom"



app = Flask(__name__, static_url_path='/static')


from app import views
