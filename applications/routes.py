from flask import render_template, redirect, url_for, flash, request, current_app
from applications import app
from applications.models import User, Photo
from applications.forms import Register_Form, Login_Form
from applications import db
from flask_login import login_user, logout_user, login_required, current_user

from flask import send_from_directory
from werkzeug.utils import secure_filename

import os

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/")
@app.route("/home")
@login_required
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
        return redirect(url_for("login_page"))
    if form.errors != {}:
        for err_msg in form.errors.values(): 
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = Login_Form()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_adress = form.email_adress.data).first()
        print("attempted user",attempted_user)
        if attempted_user and attempted_user.check_password(
                attempted_password = form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.email_adress}', category="success")
            return redirect(url_for("home_page"))
        else:
            flash("email and password are not match! Please try again", category="danger")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    print("logout")
    logout_user()
    flash("You have been logged out", category="info")
    return redirect(url_for("home_page"))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route("/upload", methods=["GET", "POST"])
def upload_page():
     if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
        file = request.files['file']
        desc = request.form.get("desc")
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            upload = Photo(filename =filename, file_src = "/uploads/" +filename, description = desc, user_id=current_user.id)
            db.session.add(upload)
            db.session.commit()
            return redirect(url_for('discover_photos'))
     return render_template("includes/upload.html")

@app.route("/delete/<id>")
@login_required
def delete(id):
    #delete db image
    image = Photo.query.get_or_404(id)
    print(id)
    print(image)
    db.session.delete(image)
    db.session.commit()
    #delete uploads folder
    os.unlink(os.path.join(current_app.root_path, 'static/uploads/' + image.filename))
    db.session.delete(image)
    db.session.commit()
    return redirect(url_for("discover_photos"))

@app.route("/photo/<id>", methods=["GET", "POST"])
@login_required
def get_image(id):
    image = Photo.query.get_or_404(id)
    if request.method == "POST":
        if image:
            image.description = request.form.get("desc")
            db.session.commit()
    return render_template("includes/photo_detail.html", photos=[image])

@app.route("/userphotos")
def user_photos():
    return render_template("includes/user_photos.html")

@app.route("/discoverphotos")
def discover_photos():
    images = Photo.query.all()
    # print(images)
    return render_template("includes/discover_photos.html", photos=images)


