from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from news_website import db, bcrypt
from news_website.users.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ResetPasswordForm, \
    UpdateAccountForm, changePassword
from news_website.models import User, UserType
from news_website.users.utils import send_reset_email

users = Blueprint("users", __name__)


class LoginPage(MethodView):
    """class for login page to get the login page and posting the data of the user for login"""

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('login.html', form=LoginForm())

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Login Successful', 'success')
                return redirect(url_for('home_page'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', form=form)


class RegistrationPage(MethodView):
    """class for getting registration page and posting the data of the user after registration"""

    def get_form(self):
        return RegistrationForm()

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('registration.html', form=RegistrationForm())

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            type_of_user = UserType.query.filter_by(type=form.user_type.data).first()
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(user_type_id=type_of_user.user_type_id, first_name=form.first_name.data,
                        last_name=form.last_name.data, gender=form.gender.data, email=form.email.data,
                        phone=form.phone.data, age=form.age.data, address=form.address.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! Now you can login to your account', 'success')
            return redirect(url_for('login_page'))
        return render_template('registration.html', form=form)


class ProfilePage(MethodView):
    """class for getting the profile page of the user"""

    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id:
            form = UpdateAccountForm()
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.email.data = current_user.email
            form.phone.data = current_user.phone
            form.age.data = current_user.age
            form.gender.data = current_user.gender
            form.address.data = current_user.address
            type_of_user = UserType.query.filter_by(user_type_id=current_user.user_type_id).first()
            return render_template('profile.html', typeOfUser=type_of_user, form=form)
        else:
            abort(403)

    def post(self, user_id):
        form = UpdateAccountForm()
        if form.validate_on_submit():
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.age = form.age.data
            current_user.gender = form.gender.data
            current_user.address = form.address.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('profile_page', user_id=current_user.id))
        type_of_user = UserType.query.filter_by(user_type_id=current_user.user_type_id).first()
        return render_template('profile.html', typeOfUser=type_of_user, form=form)


class Logout(MethodView):
    """class for user logout"""

    def get(self):
        logout_user()
        return redirect(url_for('home_page'))


class ResetPasswordRequest(MethodView):
    """class for getting the home page if user is already logged in and posting the data of password reset request form"""

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('reset_password_request.html', form=PasswordResetRequestForm())

    def post(self):
        form = PasswordResetRequestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('An email has been sent to your id please check it to reset your password.', 'info')
            return redirect(url_for('login_page'))
        return render_template('reset_password_request.html', form=form)


class ResetToken(MethodView):
    """class for getting the home page if the user is already logged in and posting the data of the user after the password reset"""

    def get(self, token):
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('reset_token.html', form=ResetPasswordForm())

    def post(self, token):
        user = User.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('reset_password_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated! You can now log in', 'success')
            return redirect(url_for('login_page'))
        return render_template('reset_token.html', form=form)


class ChangePasswordPage(MethodView):
    """class for changing password"""

    decorators = [login_required]

    def get(self):
        form = changePassword()
        return render_template('change_password.html', form=form)

    def post(self):
        form = changePassword()
        if form.validate_on_submit():

            if bcrypt.check_password_hash(current_user.password, form.password.data):
                hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
                current_user.password = hashed_password
                db.session.commit()
                flash('Password updated successfully', 'success')
                return redirect(url_for('profile_page', user_id=current_user.id))
            else:
                flash('Incorrect old password', 'danger')
        return render_template('change_password.html', form=form)
