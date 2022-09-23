from flask import Flask,render_template,request,redirect
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