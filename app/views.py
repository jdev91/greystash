import re
from app import app
from sendEmail import sendCode
from forms import LoginForm
from crypt import hashVal
from user import newUser, getUser
from flask.ext.login import current_user,login_user,logout_user,login_required
from flask import render_template, flash, url_for, request, g, redirect, session

@app.route("/")
def index():
    """Landing page for home and return from other commands"""
    return render_template('index.html')

@app.route("/logout",methods=["GET","POST"])
def logout():
    """ Removes phonenumber from cookie."""
    session["USER"] = None
    flash("Logout Succesful")
    return redirect(url_for("index"))

@app.route("/login",methods=["GET","POST"])
def login():
    """ Creates new user if needed. Then logs the user in. 
    Note:
        Stores phonenumber in a cookie
    
    """
    form = LoginForm()
    if "USER" in session.keys() and session["USER"] != None:
        flash("User already logged in\n" + str(session["USER"]))
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("login.html",form=form)
    
    if form.validate_on_submit():
        #convert phonenumber to an integer
        phoneNumber = re.sub(r'[^0-9]','',str(form.number.data))
        phoneNumer = int(phoneNumber)
        
        hashPhone = hashVal(phoneNumber)
        session["USER"] = phoneNumber
        user = newUser(hashPhone)#none if user alreay exists
        note = "Successfully Loggedin."
        
        if user == None:
            user = getUser(hashPhone)
        else:
            note = "New Account created for " + str(phoneNumber) + ".\n" + note
        flash(note)
    return redirect(request.args.get("next") or url_for("index"))
@app.route("/test",methods=["GET","POST"])
def test():
    sendCode(5039271017,123456)
