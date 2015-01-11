import re
from app import app
from sendEmail import sendCode
from forms import LoginForm, GenPassForm
from crypt import hashVal
from user import newUser, getUser, getCode, createSalts, setSalts
from flask.ext.login import current_user,login_user,logout_user,login_required
from flask import render_template, flash, url_for, request, g, redirect, session, jsonify

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
        
        #user is trying to generate a password
        if user == None:
            user = getUser(hashPhone)
            flash(note)
            return redirect(url_for("getCode", phoneNumber = str(phoneNumber)))
        
        #user is creating an account
        note = "New Account created for " + str(phoneNumber) + ".\n" + note
        flash(note)
    return redirect(request.args.get("next") or url_for("login"))

@app.route("/genCode/<phoneNumber>/sendCode",methods=["GET", "POST"])
def getCode(phoneNumber):
    phoneHash = hashVal(phoneNumber) 
    user = newUser(phoneHash)#none if user alreay exists
    if user == None:
        user = getUser(phoneHash)
    print(str(user))
    code = user.updateCode()
    print("Sending code value: " + str(code))
    sendCode(phoneNumber,code)
    return redirect(url_for("genCode",phoneNumber=str(phoneNumber)))

@app.route("/genCode/<phoneNumber>",methods=["GET", "POST"])
def genCode(phoneNumber):
    user = getUser(hashVal(phoneNumber))
    print("Current user: " + str(user))
    form = GenPassForm(user = user)
    if request.method == "GET":
        return render_template("genCode.html",form=form)
    if form.validate_on_submit():
        #gen password
        if not user.checkCode(int(form.code.data)):
            flash("One time code does not match. Please try again.")
            return redirect(url_for("genCode",phoneNumber = str(phoneNumber)))
        password = user.genPass(form.url.data,True)
        flash("Password for " + form.url.data + " is " + str(password))
    return redirect(url_for("login"))

@app.route("/api/<phoneNumber>/<code>/<url>")
def apiGenPass(phoneNumber, code, url):
    user = getUser(hashVal(phoneNumber))
    if not user or not user.checkCode(int(code)):
        return jsonify({"msg" : "failed"})
    createSalts(user, url)
    return jsonify({"msg" : user.genPass(url,True)})

@app.route("/api/new/<phoneNumber>/<code>/<url>")
def apiGenNewPass(phoneNumber, code, url):
    user = getUser(hashVal(phoneNumber))
    if not user or not user.checkCode(int(code)):
        return jsonify({"msg" : "failed"})
    createSalts(user, url)
    return jsonify({"msg" : user.genPass(url,False)})

@app.route("/api/update/<phoneNumber>/<url>/<code>")
def apiUpdatePass(phoneNumber,url,code):
    user = getUser(hashVal(phoneNumber))
    if not user or not user.checkCode(int(code)):
        return jsonify({"msg" : "failed"})
    createSalts(user, url)
    vals = user.updateSalt(url)
    print("Update vals: " + str(vals))
    setSalts(user,url,vals)
    return jsonify({"msg" : "success"})

@app.route("/api/isStale/<phoneNumber>/<url>")
def apiIsStale(phoneNumber,url):
    user = getUser(hashVal(phoneNumber))
    if not user :
        return jsonify({"msg" : "failed"})
    createSalts(user, url)
    return jsonify({"msg" : str(user.isStale(url))})

#handle cors requests
@app.before_request
def before_request():
    g.user = current_user
    if request.method == 'OPTIONS' and True:
        resp = app.make_default_options_response()
    
        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
        
        h = resp.headers
    
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']
            
        h = resp.headers
        
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Req']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp

#add CORS headers
@app.after_request
def add_cors(resp):
    """ Ensure all responses have the CORS headers. This ensures any failures are also accessible
    by the client. """

    resp.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin','*')
    resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    resp.headers['Access-Control-Allow-Headers'] = request.headers.get( 
    'Access-Control-Request-Headers', 'Authorization' )
    # set low for debugging
    if app.debug:
        resp.headers['Access-Control-Max-Age'] = '1'
    return resp
