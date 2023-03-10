from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

UPLOAD_FOLDER = 'applications/static/uploads/'

app = Flask(__name__)

import os
from dotenv import load_dotenv
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///applications.db"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

secret_key = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = {secret_key}

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from applications import routes