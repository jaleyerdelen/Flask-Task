from flask import render_template, redirect, url_for, flash
from applications import app
from applications.models import User
from applications.forms import Register_Form
from applications import db

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = Register_Form()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                              email_adress = form.email_adress.data,
                              password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account created successfully! You are now logged in as: {user_to_create.username}', category="success")
        return redirect(url_for("home_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template("register.html", form=form)
