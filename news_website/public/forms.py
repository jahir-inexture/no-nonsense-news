from flask_wtf import FlaskForm
from wtforms import SubmitField


class CategoryFilterForm(FlaskForm):
    """form for category filtering"""
    search = SubmitField('Search')
