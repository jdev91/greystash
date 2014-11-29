from flask.ext.wtf import Form
from wtforms import StringField, BooleanField

class LoginForm(Form):
    number = StringField("Phone number")
    def validate_on_submit(self):
        return True
