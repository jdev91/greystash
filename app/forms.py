from flask.ext.wtf import Form
from wtforms import StringField, BooleanField

class LoginForm(Form):
    uID = StringField("Secret phrase")
    remberMe = BooleanField("Remember me",default=False)
    
    def validate_on_submit(self):
        return True
