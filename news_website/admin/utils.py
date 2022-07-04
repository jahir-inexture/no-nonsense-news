from flask import request, url_for
from wtforms import ValidationError
from news_website.models import NewsCategory, News, NewsImageMapping, JournalistNewsMapping


def check_category(self, field):
    """function for checking whether the newly added category already exists or not"""
    category_obj = NewsCategory.query.filter_by(category=field.data.title()).first()
    if category_obj:
        raise ValidationError('Category already exists please choose a different one.')


def get_distinct_news_category():
    """function for getting distinct news category id from the news table"""
    distinct_news_category = News.query.with_entities(News.news_category_id).distinct().all()
    return [i[0] for i in distinct_news_category]


def get_filtered_news(news_obj):
    """function for getting filtered news"""

    news_data_dict = {}
    for data in news_obj.items:
        news_data_dict[data.news_id] = {}
        news_data_dict[data.news_id]["data"] = data
        author = JournalistNewsMapping.query.filter_by(news_id=data.news_id).first()
        news_data_dict[data.news_id]["author_id"] = author.journalistnews.id
        news_data_dict[data.news_id]["author_first_name"] = author.journalistnews.first_name
        news_data_dict[data.news_id]["author_last_name"] = author.journalistnews.last_name
        img_obj = NewsImageMapping.query.filter_by(news_id=data.news_id).all()
        news_data_dict[data.news_id]["images"] = []
        if img_obj:
            for img in img_obj:
                # image_file = url_for('static', filename='news_images/' + img.image)
                news_data_dict[data.news_id]["images"].append(img.image)

    return news_data_dict
