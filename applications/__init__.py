from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from applications import routes

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///applications.db"
db = SQLAlchemy(app)

