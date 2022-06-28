from datetime import date
from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask.views import MethodView
from flask_login import login_required, current_user
from news_website import db
from news_website.admin.forms import FilterForm
from news_website.models import PremiumUserMapping
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
            # else:
            #     return redirect(url_for('subscribe', user_id=current_user.id))

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
