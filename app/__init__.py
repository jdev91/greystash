from flask import Flask
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    MAIL_SERVER='smtp.live.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'greystash.devlin@hotmail.com',
    MAIL_PASSWORD = 'Foobaryo',
    MONGOALCHEMY_DATABASE = "Users",
    SECRET_KEY = "kjlsfdjlksdfjlksdfjkfsdjlksdfjk"
)

lm = LoginManager()
lm.init_app(app)
db = MongoAlchemy(app)
mail = Mail(app)
from views import *
from user import *
from crypt import *
from forms import *
from sendEmail import *
