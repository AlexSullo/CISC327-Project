from qbnb import *
from curses.ascii import isalnum
from qbnb.models import *
from flask import Flask, redirect, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route("/")
def home():

    return render_template('homepage.html')


@app.route("/listing")
def listing():

    return render_template('listing.html')


@app.route("/settings")
def settings():
    return render_template('settings.html')

