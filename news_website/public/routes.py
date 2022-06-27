from flask import Blueprint, render_template
from flask.views import MethodView

from news_website.admin.forms import FilterForm
from news_website.public.utils import get_news

public = Blueprint("public", __name__)


class ShowNews(MethodView):
    def get(self, category):
        news_dict_data, news_data = get_news(category.title())
        return render_template('show_public_news.html', news_dict_data=news_dict_data, news_data=news_data,
                               category=category)

