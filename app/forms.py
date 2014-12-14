from app import *
from user import *
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField

class LoginForm(Form):
    number = StringField("Phone number")
    def validate_on_submit(self):
        return True
class GenPassForm(Form):
    code = StringField("Phone number")
    url = StringField("Website URL")
    typedPass = PasswordField("Typed Password")
    def validate_on_submit(self):
        return True

