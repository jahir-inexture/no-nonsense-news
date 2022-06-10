from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask.views import MethodView
from flask_login import current_user, login_required, login_user, logout_user
from news_website import db, bcrypt
from news_website.users.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ResetPasswordForm
from news_website.models import User, userType
from news_website.users.utils import send_reset_email

users = Blueprint("users", __name__)


class loginPage(MethodView):
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


class registrationPage(MethodView):

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('home_page'))
        return render_template('registration.html', form=RegistrationForm())

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            ut = userType.query.filter_by(type=form.user_type.data).first()
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(user_type_id=ut.user_type_id, fname=form.fname.data, lname=form.lname.data,
                        gender=form.gender.data,
                        email=form.email.data, phone=form.phone.data, age=form.age.data, address=form.address.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! Now you can login to your account', 'success')
            return redirect(url_for('login_page'))
        return render_template('registration.html', form=form)


class profilePage(MethodView):
    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id:
            type_of_user = userType.query.filter_by(user_type_id=current_user.user_type_id).first()
            return render_template('profile.html', typeOfUser=type_of_user)
        else:
            abort(403)


class logout(MethodView):
    def get(self):
        logout_user()
        return redirect(url_for('home_page'))


class resetPasswordRequest(MethodView):
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


class resetToken(MethodView):

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
