from flask import Flask
app = Flask(__name__)
app.config.update(
    DEBUG=True
)
from views import *
