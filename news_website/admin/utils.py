from wtforms import ValidationError

from news_website.models import newsCategory, News


def check_category(self, field):
    """function for checking whether the newly added category already exists or not"""
    category_obj = newsCategory.query.filter_by(category=field.data.title()).first()
    if category_obj:
        raise ValidationError('Category already exists please choose a different one.')


def get_distinct_news_category():
    """function for getting distinct news category id from the news table"""
    distinct_news_category = News.query.with_entities(News.news_category_id).distinct().all()
    return [i[0] for i in distinct_news_category]
