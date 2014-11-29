from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mongoalchemy import MongoAlchemy

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    MONGOALCHEMY_DATABASE = "Users",
    SECRET_KEY = "kjlsfdjlksdfjlksdfjkfsdjlksdfjk"
)

lm = LoginManager()
lm.init_app(app)
db = MongoAlchemy(app)
from views import *
from user import *
from crypt import *
from forms import *
