import subprocess
from flask import Blueprint, redirect, url_for, render_template, abort, request, flash
from flask.views import MethodView
from flask_login import login_required, current_user
from news_website import db
from news_website.admin.forms import AddCategoryForm, FilterForm
from news_website.admin.utils import get_distinct_news_category, get_filtered_news
from news_website.models import News, JournalistNewsMapping, NewsImageMapping, User, NewsCategory

admin = Blueprint("admin", __name__)


class CheckArticlesPage(MethodView):
    """class for checking articles to approve or not for admin"""
    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id and current_user.usertype.type == "admin":
            news_data_dict = {}
            page = request.args.get('page', 1, type=int)
            news_raw_data = News.query.filter_by(checked=False).order_by(News.news_date).paginate(page=page,
                                                                                                  per_page=5)
            for data in news_raw_data.items:
                news_data_dict[data.news_id] = {}
                author = JournalistNewsMapping.query.filter_by(news_id=data.news_id).first()
                news_data_dict[data.news_id]["author_id"] = author.journalist_id
                news_data_dict[data.news_id]["author_first_name"] = author.journalistnews.first_name
                news_data_dict[data.news_id]["author_last_name"] = author.journalistnews.last_name
                news_data_dict[data.news_id]["news_id"] = data.news_id
                news_data_dict[data.news_id]["news_heading"] = data.news_heading
                news_data_dict[data.news_id]["news_info"] = data.news_info
                news_data_dict[data.news_id]["news_date"] = data.news_date.date()
                news_data_dict[data.news_id]["news_category"] = data.categorytype.category
                news_images = NewsImageMapping.query.filter_by(news_id=data.news_id).all()
                news_data_dict[data.news_id]["images"] = []
                if news_images:
                    for one_image in news_images:
                        news_data_dict[data.news_id]["images"].append(one_image.image)

            return render_template('check_articles.html', news_data_dict=news_data_dict, news_raw_data=news_raw_data)
        else:
            abort(403)


class ApproveArticle(MethodView):
    """class for approving articles for admin"""
    decorators = [login_required]

    def get(self, user_id, news_id):
        if user_id == current_user.id and current_user.usertype.type == "admin":

            news_obj = News.query.filter_by(news_id=news_id).first()
            news_obj.checked = True
            news_obj.is_approved = True
            db.session.commit()
            return redirect(url_for('check_articles', user_id=current_user.id))
        else:
            abort(403)


class DeclineArticle(MethodView):
    """class for declining articles for admin"""
    decorators = [login_required]

    def get(self, user_id, news_id):
        if user_id == current_user.id and current_user.usertype.type == "admin":

            news_obj = News.query.filter_by(news_id=news_id).first()
            news_obj.checked = True
            news_obj.is_approved = False
            db.session.commit()
            return redirect(url_for('check_articles', user_id=current_user.id))
        else:
            abort(403)


class ShowAllArticles(MethodView):
    """class for showing articles that are approved"""
    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id and current_user.usertype.type == "admin":
            page = request.args.get('page', 1, type=int)
            news_obj = News.query.filter_by(scraped_data=False).order_by(News.news_date).paginate(page=page,
                                                                                                  per_page=5)
            news_data_dict = get_filtered_news(news_obj)
            return render_template('show_all_articles.html', news_data_dict=news_data_dict, news_obj=news_obj,
                                   form=FilterForm())
        else:
            abort(403)

    def post(self, user_id):
        form = FilterForm()
        return redirect(url_for('show_filtered_articles', filter=form.filter_articles.data, user_id=current_user.id))


class ShowFilteredArticles(MethodView):
    """class for showing filtered articles for admin"""
    decorators = [login_required]

    def get(self, user_id, filter):
        page = request.args.get('page', 1, type=int)

        if filter == "all_articles":
            news_obj = News.query.filter_by(scraped_data=False).order_by(News.news_date).paginate(page=page,
                                                                                                  per_page=5)
        elif filter == "approved":
            news_obj = News.query.filter_by(scraped_data=False, checked=True, is_approved=True).order_by(
                News.news_date).paginate(page=page, per_page=5)

        elif filter == "not_approved":
            news_obj = News.query.filter_by(scraped_data=False, checked=True, is_approved=False).order_by(
                News.news_date).paginate(page=page, per_page=5)

        elif filter == "checked":
            news_obj = News.query.filter_by(scraped_data=False, checked=True).order_by(
                News.news_date).paginate(page=page, per_page=5)

        elif filter == "not_checked":
            news_obj = News.query.filter_by(scraped_data=False, checked=False).order_by(
                News.news_date).paginate(page=page, per_page=5)

        news_data_dict = get_filtered_news(news_obj)
        return render_template('show_filtered_articles.html', news_data_dict=news_data_dict, news_obj=news_obj,
                               filter=filter)


class ShowArticlesByJournalist(MethodView):
    """class for showing articles of corresponding journalist"""

    def get(self, user_id, journalist_id):
        if user_id == current_user.id and current_user.usertype.type == "admin":
            page = request.args.get('page', 1, type=int)

            journalist_news_id_list = User.query \
                .join(JournalistNewsMapping, User.id == JournalistNewsMapping.journalist_id) \
                .add_columns(JournalistNewsMapping.news_id) \
                .filter(User.id == journalist_id).paginate(page=page, per_page=5)
            news_dict = {}
            images_dict = {}
            for articles in journalist_news_id_list.items:
                news_list = News.query.filter_by(news_id=articles[1]).first()
                images_list = NewsImageMapping.query.filter_by(news_id=articles[1]).all()
                news_dict[news_list.news_id] = news_list
                images_dict[news_list.news_id] = []
                for one_image in images_list:
                    images_dict[news_list.news_id].append(one_image.image)

            return render_template('show_journalist_article.html', news_dict=news_dict, images_dict=images_dict,
                                   journalist_news_id_list=journalist_news_id_list)
        else:
            abort(403)


class AddCategory(MethodView):
    """Class for adding new news category"""

    def get(self, user_id):
        if user_id == current_user.id and current_user.usertype.type == "admin":
            return render_template("add_category.html", categories=NewsCategory.query.all(), form=AddCategoryForm(),
                                   category_count=NewsCategory.query.count(),
                                   distinct_news_list=get_distinct_news_category())
        else:
            abort(403)

    def post(self, user_id):
        form = AddCategoryForm()
        if form.validate_on_submit():
            add_category = NewsCategory(category=form.news_type.data.title())
            db.session.add(add_category)
            db.session.commit()
            return redirect(url_for('add_category', user_id=current_user.id))

        return render_template("add_category.html", categories=NewsCategory.query.all(), form=form,
                               category_count=NewsCategory.query.count(),
                               distinct_news_list=get_distinct_news_category())


class DeleteCategory(MethodView):
    """Class for deleting category"""

    def get(self, user_id, categoryId):
        if user_id == current_user.id and current_user.usertype.type == "admin":
            category_obj = NewsCategory.query.filter_by(category_id=categoryId).first()
            db.session.delete(category_obj)
            db.session.commit()
            return redirect(url_for('add_category', user_id=current_user.id))
        else:
            abort(403)


class ScrapData(MethodView):
    """class for scraping data"""

    def get(self):
        if current_user.usertype.type == "admin":
            subprocess.check_output(['python', '-m',
                                     'news_website.scraping.indianexpress_politics_scraper.indianexpress_politics_scraper.spiders.politics_spider'])
            flash('Loading Data... Please wait for 5-10 seconds.', 'info')
            return redirect(url_for('home_page'))
        else:
            abort(403)
