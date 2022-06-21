from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, MultipleFileField, SelectField
from wtforms.validators import DataRequired, Length
from news_website.models import newsCategory


class PostArticlesForm(FlaskForm):
    """form for posting articles for journalist"""
    title = StringField('Title', validators=[DataRequired(), Length(min=10, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Post')


class ArticlesImageUploadForm(FlaskForm):
    """forms for posting multiple images"""
    picture = MultipleFileField('Upload Images')


class UpdateArticlesForm(FlaskForm):
    """form for updating articles posted by journalist"""

    title = StringField('Title', validators=[DataRequired(), Length(min=10, max=200)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    picture = MultipleFileField('Upload Images')

    submit = SubmitField('Update')
