from news_website.models import NewsCategory, News, NewsImageMapping


def get_latest_news_for_home_page(category_of_news):
    news_category = NewsCategory.query.filter_by(category=category_of_news).first()
    news_data = News.query.filter_by(news_category_id=news_category.category_id, scraped_data=True).order_by(
        News.news_date.desc()).limit(3).all()
    news_dict_data = {}
    for news in news_data:
        news_dict_data[news.news_id] = {}
        news_dict_data[news.news_id]["data"] = news
        images_data = NewsImageMapping.query.filter_by(news_id=news.news_id).first()
        news_dict_data[news.news_id]["image"] = images_data.image
    return news_dict_data, news_data
