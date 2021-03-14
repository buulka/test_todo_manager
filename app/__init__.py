from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)

from app import routes

login = LoginManager(app)

