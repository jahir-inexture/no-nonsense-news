from flask import url_for
from flask_mail import Message
from wtforms.validators import ValidationError
from news_website import mail
import re


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender=('No Nonsense News', 'nonsense@news.com'),
                  recipients=[user.email])
    msg.body = f'''Click on the following link to reset your password:
{url_for('reset_token', token=token, _external=True)}
If you didn't send this password reset request then please ignore this mail'''

    mail.send(msg)


def valid_number(self, field):
    if not re.fullmatch('[6-9][0-9]{9}', field.data):
        raise ValidationError('Enter proper phone number starting from 6,7,8 or 9.')


def valid_password(self, field):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,18}$"
    if not re.fullmatch(reg, field.data):
        raise ValidationError(
            'Enter password such that it contains 1 Uppercase, 1 Lowercase, 1 special character and 1 number.')


def validate_name(self, field):
    if not field.data.isalpha():
        raise ValidationError('Please Enter proper name only including alphabets.')
