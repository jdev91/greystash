from flask import Flask
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_USE_SSL = False,
    MAIL_USE_TLS = False,
    MAIL_Port = 465,
    MAIL_USERNAME="greystashthethird@gmail.com",
    MAIL_PASSWORD="ljmj2310",
    DEBUG = True,
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
