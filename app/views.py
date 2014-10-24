from app import app, user
from flask import render_template

@app.route("/")
def index():
    """Landing page for home and return from other commands"""
    return render_template('index.html')

@app.route("/login")
def login():
    form = LoginForm()
    if form.validate_on_subimt():
        print("Form is valid")
    else:
        print("Form is not valid")
    return render_tempalte('index.html')
    
