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
    MAIL_PASSWORD = 'Tdpd8dBNsdiuy1dp',
    MONGOALCHEMY_DATABASE = "Users10",
    SECRET_KEY = "fjk)7h,>iqEdiuoasdkjnbkljhd88923)HI2Mmlk2oOAIHasdl//"
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
