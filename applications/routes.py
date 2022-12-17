from flask import render_template
from applications import app
from applications.models import User

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")
