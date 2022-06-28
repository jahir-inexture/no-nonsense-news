from datetime import date
from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask.views import MethodView
from flask_login import login_required, current_user
from news_website import db
from news_website.admin.forms import FilterForm
from news_website.models import PremiumUserMapping, News, NewsImageMapping, JournalistNewsMapping, User
from news_website.public.utils import get_news
from dateutil.relativedelta import relativedelta

public = Blueprint("public", __name__)


class ShowNews(MethodView):
    def get(self, category):
        news_dict_data, news_data = get_news(category.title())
        return render_template('show_public_news.html', news_dict_data=news_dict_data, news_data=news_data,
                               category=category)


class Subscribe(MethodView):
    decorators = [login_required]

    def get(self, user_id):
        if current_user.id == user_id:
            three_mon_rel = relativedelta(months=3)
            premium_user = PremiumUserMapping.query.filter_by(user_id=current_user.id).first()
            if premium_user:
                days_left = ((premium_user.purchase_date.date() + three_mon_rel) - date.today()).days
                if days_left >= 0:
                    return render_template('subscribed_user.html', days_left=days_left, premium_user=premium_user)
                else:
                    db.session.delete(premium_user)
                    db.session.commit()
                    return render_template('subscribe.html')
            else:
                return render_template('subscribe.html')

        else:
            abort(403)


class BuySubscription(MethodView):
    decorators = [login_required]

    def get(self, user_id):
        if current_user.id == user_id:
            current_user.has_premium = True
            subscribed_user = PremiumUserMapping(user_id=current_user.id, purchase_date=date.today())
            db.session.add(subscribed_user)
            db.session.commit()
            flash('Congrats, now you are a premium user!!!', 'success')
            return redirect(url_for('subscribe', user_id=current_user.id))
        else:
            abort(403)


class GetJournalistAllArticles(MethodView):
    """class for getting all the articles posted by journalist which is approved by the admin which will be shown publicly"""

    def get(self):
        page = request.args.get('page', 1, type=int)
        raw_data = News.query.filter_by(scraped_data=False, checked=True, is_approved=True).order_by(
            News.news_date.desc()).paginate(page=page, per_page=5)
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

        return render_template('journalist_articles.html', news_dict=news_dict, raw_data=raw_data)


class GetJournalistArticles(MethodView):
    """class for getting specific journalist articles"""

    def get(self, journalist_id):
        page = request.args.get('page', 1, type=int)
        journalist_data = User.query.filter_by(id=journalist_id).first()
        journalist_news = JournalistNewsMapping.query.filter_by(journalist_id=journalist_id).paginate(page=page,
                                                                                                      per_page=5)
        news_dict = {}
        for data in journalist_news.items:
            news_data = News.query.filter_by(news_id=data.news_id, checked=True, is_approved=True).first()
            if news_data:
                news_dict[news_data.news_id] = {}
                news_dict[news_data.news_id]["heading"] = news_data.news_heading
                news_dict[news_data.news_id]["content"] = news_data.news_info
                news_dict[news_data.news_id]["date"] = news_data.news_date
                images_data = NewsImageMapping.query.filter_by(news_id=news_data.news_id).all()
                news_dict[data.news_id]["image"] = []
                for images in images_data:
                    image_file = url_for('static', filename='news_images/' + images.image)
                    news_dict[data.news_id]["image"].append(image_file)
            print(news_dict)
        return render_template('articles_by_journalist.html', news_dict=news_dict, journalist_news=journalist_news,
                               journalist_data=journalist_data)
