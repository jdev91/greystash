from app import *
from user import *
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField

class LoginForm(Form):
    number = StringField("Phone number")
    def validate_on_submit(self):
        return True
class GenPassForm(Form):
    code = StringField("Code")
    url = StringField("Website URL")
    typedPass = PasswordField("Typed Password")
    user = None
    def validate_on_submit(self):
        if user == None:
            return False
        if user.oneTimeKey == code:
            return True
        return False

