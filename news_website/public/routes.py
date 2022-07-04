import os
from datetime import date
import stripe
from flask import Blueprint, render_template, abort, flash, redirect, url_for, request
from flask.views import MethodView
from flask_login import login_required, current_user
from news_website import db
from news_website.models import PremiumUserMapping, News, NewsImageMapping, JournalistNewsMapping, User, NewsCategory
from news_website.public.forms import CategoryFilterForm
from news_website.public.utils import get_news, get_news_by_object, get_news_for_newsletter, get_latest_news, \
    get_latest_news_image
from dateutil.relativedelta import relativedelta

public = Blueprint("public", __name__)
stripe_keys = {
    'secret_key': os.environ['STRIPE_SECRET_KEY'],
    'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']


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
                    current_user.has_premium = False
                    db.session.delete(premium_user)
                    db.session.commit()
                    return render_template('subscribe.html')
            else:
                return render_template('subscribe.html')

        else:
            abort(403)


class Payment(MethodView):
    """class for payment of buying subscription"""
    decorators = [login_required]

    def get(self, user_id):
        if current_user.id == user_id:

            return render_template('payment.html', key=stripe_keys['publishable_key'])
        else:
            abort(403)


class Checkout(MethodView):
    """class for checkout after payment"""
    decorators = [login_required]

    def post(self, user_id):
        if current_user.id == user_id:
            amount = 199 * 100

            customer = stripe.Customer.create(
                email=current_user.email,
                source=request.form['stripeToken']
            )

            stripe.PaymentIntent.create(
                customer=customer.id,
                amount=amount,
                currency='inr',
                description='No Nonsense News Subscription Charge'
            )

            current_user.has_premium = True
            subscribed_user = PremiumUserMapping(user_id=current_user.id, purchase_date=date.today())
            db.session.add(subscribed_user)
            db.session.commit()
            flash('Congrats, now you are a premium user!!!', 'success')

            return render_template('checkout.html', amount=amount)
        else:
            abort(403)


class GetJournalistAllArticles(MethodView):
    """class for getting all the articles posted by journalist which is approved by the admin which will be shown publicly"""

    def get(self):
        form = CategoryFilterForm()
        page = request.args.get('page', 1, type=int)
        raw_data = News.query.filter_by(scraped_data=False, checked=True, is_approved=True).order_by(
            News.news_date.desc()).paginate(page=page, per_page=5)
        news_dict = get_news_by_object(raw_data)

        return render_template('journalist_articles.html', news_dict=news_dict, raw_data=raw_data,
                               categories=NewsCategory.query.all(), form=form)

    def post(self):
        form = CategoryFilterForm()
        category_id = request.form.get('category')
        return redirect(url_for('filtered_articles', category_id=category_id))


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
                    news_dict[data.news_id]["image"].append(images.image)
        return render_template('articles_by_journalist.html', news_dict=news_dict, journalist_news=journalist_news,
                               journalist_data=journalist_data)


class FilteredArticles(MethodView):
    """class for getting filter news"""

    def get(self, category_id):
        page = request.args.get('page', 1, type=int)
        raw_data = News.query.filter_by(checked=True, is_approved=True, news_category_id=category_id).order_by(
            News.news_date.desc()).paginate(page=page, per_page=5)
        news_dict = get_news_by_object(raw_data)
        return render_template('filtered_articles.html', news_dict=news_dict, raw_data=raw_data,
                               category_name=NewsCategory.query.filter_by(category_id=category_id).first(),
                               category_id=category_id)


class NewsLetter(MethodView):
    """class for generating newsletter for premium user"""

    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id:
            carousel_dict = {"first-slide": get_latest_news("Politics"),
                             "first-slide-image": get_latest_news_image(get_latest_news("Politics").news_id),
                             "second-slide": get_latest_news("Entertainment"),
                             "second-slide-image": get_latest_news_image(get_latest_news("Entertainment").news_id),
                             "third-slide": get_latest_news("Sports"),
                             "third-slide-image": get_latest_news_image(get_latest_news("Sports").news_id),
                             "fourth-slide": get_latest_news("Education"),
                             "fourth-slide-image": get_latest_news_image(get_latest_news("Education").news_id)}

            politics_news_dict = get_news_for_newsletter("Politics")
            entertainment_news_dict = get_news_for_newsletter("Entertainment")
            sports_news_dict = get_news_for_newsletter("Sports")
            education_news_dict = get_news_for_newsletter("Education")
            news_list = [("Politics", politics_news_dict), ("Entertainment", entertainment_news_dict),
                         ("Sports", sports_news_dict), ("Education", education_news_dict)]
            category_list = ["Politics", "Entertainment", "Sports", "Education"]
            return render_template('newsletter.html', news_list=news_list, category_list=category_list,
                                   carousel_dict=carousel_dict)
        else:
            abort(403)
