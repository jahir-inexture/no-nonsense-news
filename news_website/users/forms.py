from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, RadioField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from news_website.models import User
from news_website.users.utils import valid_number, valid_password, validate_name


class RegistrationForm(FlaskForm):
    """Registration form for user registration"""
    user_type = RadioField('Who are you?', choices=[('user', 'User'), ('journalist', 'Journalist')])
    first_name = StringField('First Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    gender = RadioField('Select Gender', choices=[('male', 'Male'), ('female', 'Female')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), valid_number, Length(min=10, max=10)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(16, 200)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    password = PasswordField('Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_phone(self, phone):
        """function for validating existing phone number """

        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_email(self, email):
        """function for validating existing email """

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """login form for user login"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Form for updating user details"""
    first_name = StringField('First Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    gender = RadioField('Select Gender', choices=[('male', 'Male'), ('female', 'Female')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), valid_number, Length(min=10, max=10)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(16, 200)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('Update Details')

    def validate_phone(self, phone):
        """function for validating existing phone number of other user"""

        user = User.query.filter_by(phone=phone.data).first()
        if user:
            if user.phone != current_user.phone:
                raise ValidationError('That phone number is taken. Please choose a different one.')

    def validate_email(self, email):
        """function for validating existing email of other user"""

        user = User.query.filter_by(email=email.data).first()
        if user:
            if user.email != current_user.email:
                raise ValidationError('That email is taken. Please choose a different one.')


class PasswordResetRequestForm(FlaskForm):
    """Password reset request form where user can request for password reset by submitting his/her email"""
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        """checking if the user requesting for password change by submitting email is registered with that email or not"""
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first')


class ResetPasswordForm(FlaskForm):
    """Password reset form for changing password after requesting for password reset"""
    password = PasswordField('Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class changePassword(FlaskForm):
    """Change password form for changing the password"""
    password = PasswordField('Password',
                             validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), valid_password, Length(min=6, max=18)])
    submit = SubmitField('Change Password')
