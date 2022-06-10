from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from news_website.models import User
from news_website.users.utils import valid_number, valid_password, validate_name


class RegistrationForm(FlaskForm):
    user_type = RadioField('Who are you?', choices=[('user', 'User'), ('journalist', 'Journalist')])
    fname = StringField('First Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    lname = StringField('Last Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    gender = RadioField('Select Gender', choices=[('male', 'Male'), ('female', 'Female')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), valid_number, Length(min=10, max=10)])
    age = IntegerField('Age', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    password = PasswordField('Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_phone(self, phone):

        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
