from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from applications.models import User

class Register_Form(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")

    def validate_email_adress(self, email_adress_to_check):
        email_adress = User.query.filter_by(email_adress = email_adress_to_check.data).first()
        if email_adress:
            raise ValidationError("Email address already exists! Please try a different email address")

    username = StringField(label = "User Name", validators=[DataRequired()])
    email_adress = StringField(label = "Email Adress" ,validators=[DataRequired()])
    password1 = PasswordField(label = "Password", validators=[Length(min=5), DataRequired()])
    password2 = PasswordField(label = "Confirm Password", validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label = "Sign in")
