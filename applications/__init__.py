from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

import os
from dotenv import load_dotenv
load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///applications.db"
secret_key = os.getenv("SECRET_KEY")
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = {secret_key}


from applications import routes