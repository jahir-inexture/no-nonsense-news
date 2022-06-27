from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Length
from news_website.admin.utils import check_category


class AddCategoryForm(FlaskForm):
    """class for creating form for adding category"""
    news_type = StringField('Add New Category', validators=[Length(min=2, max=20), check_category])
    submit = SubmitField('Add')


class FilterForm(FlaskForm):
    """class for creating form used for filtering data"""
    filter = SelectField('Filter By', choices=[('all_articles', 'Show all articles'), ('filter_approved', 'Approved'),
                                               ('filer_not_approved', 'NotApproved')])
    search = SubmitField('search')
