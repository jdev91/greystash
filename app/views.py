from app import app
from flask import render_template

@app.route("/")
def index():
    """Landing page for home and return from other commands"""
    return render_template('index.html')
