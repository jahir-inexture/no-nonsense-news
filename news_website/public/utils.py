from flask import request, url_for
from news_website.models import NewsCategory, News, NewsImageMapping, JournalistNewsMapping


def get_news(category_of_news):
    """function for fetching news for particular category and storing that news in dictionary and returning that dictionary"""
    news_category = NewsCategory.query.filter_by(category=category_of_news).first()
    page = request.args.get('page', 1, type=int)
    news_data = News.query.filter_by(news_category_id=news_category.category_id, scraped_data=True).order_by(
        News.news_date.desc()).paginate(page=page, per_page=5)
    news_dict_data = generate_news_dict(news_data)
    return news_dict_data, news_data


def generate_news_dict(news_data):
    news_dict_data = {}
    for news in news_data.items:
        news_dict_data[news.news_id] = {}
        news_dict_data[news.news_id]["data"] = news
        images_data = NewsImageMapping.query.filter_by(news_id=news.news_id).first()
        news_dict_data[news.news_id]["image"] = images_data.image
    return news_dict_data


def get_news_by_object(raw_data):
    news_dict = {}

    for data in raw_data.items:
        news_dict[data.news_id] = {}
        news_dict[data.news_id]["heading"] = data.news_heading
        news_dict[data.news_id]["content"] = data.news_info
        news_dict[data.news_id]["date"] = data.news_date
        author = JournalistNewsMapping.query.filter_by(news_id=data.news_id).first()
        news_dict[data.news_id]["author"] = author
        news_dict[data.news_id]["image"] = []
        images_data = NewsImageMapping.query.filter_by(news_id=data.news_id).all()
        for images in images_data:
            image_file = url_for('static', filename='news_images/' + images.image)
            news_dict[data.news_id]["image"].append(image_file)
    return news_dict


def get_news_for_newsletter(category_of_news):
    news_category = NewsCategory.query.filter_by(category=category_of_news).first()
    news_data = News.query.filter_by(news_category_id=news_category.category_id, scraped_data=True).order_by(
        News.news_date.desc()).limit(5).all()
    news_dict_data = {}
    for news in news_data:
        news_dict_data[news.news_id] = {}
        news_dict_data[news.news_id]["data"] = news
        images_data = NewsImageMapping.query.filter_by(news_id=news.news_id).first()
        news_dict_data[news.news_id]["image"] = images_data.image
    return news_dict_data
