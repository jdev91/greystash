import re
from app import app
from sendEmail import sendCode
from forms import LoginForm, GenPassForm
from crypt import hashVal
from user import newUser, getUser, getCode
from flask.ext.login import current_user,login_user,logout_user,login_required
from flask import render_template, flash, url_for, request, g, redirect, session

@app.route("/")
def index():
    """Landing page for home and return from other commands"""
    return render_template('index.html')


@app.route("/login",methods=["GET","POST"])
def login():
    """ Creates new user if needed. Then logs the user in. 
    Note:
        Stores phonenumber in a cookie
    
    """
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html",form=form)
    
    if form.validate_on_submit():
        #convert phonenumber to an integer
        phoneNumber = re.sub(r'[^0-9]','',str(form.number.data))
        phoneNumer = int(phoneNumber)
        
        hashPhone = hashVal(phoneNumber)
        user = newUser(hashPhone)#none if user alreay exists
        note = "Successfully Loggedin."
        
        if user == None:
            user = getUser(hashPhone)
        else:
            note = "New Account created for " + str(phoneNumber) + ".\n" + note
        flash(note)
        return redirect(url_for("genCode",phoneNumber 
            = str(phoneNumber), code = "NONE"))
    return redirect(request.args.get("next") or url_for("login"))

@app.route("/genCode/<phoneNumber>/<code>",methods=["GET", "POST"])
def genCode(phoneNumber,code):
    user = getUser(phoneNumber)
    form = GenPassForm(user = user)
    if request.method == "GET" or code == "NONE":
        #update users one time ddcode
        code = getCode()
        sendCode(phoneNumber,code)
        return render_template("genCode.html",form=form)
    
    if form.validate_on_submit():
        #gen password
        password = "Dummy"
        flash("Password for " + form.url.data + " is " + password)
    else:
        flash("Wrong code. A new one is being sent")
    return render_template("genCode.html")


@app.route("/test",methods=["GET","POST"])
def test():
    sendCode(5039271017,123456)
