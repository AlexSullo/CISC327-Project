from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")

def home():
    return render_template('homepage.html')