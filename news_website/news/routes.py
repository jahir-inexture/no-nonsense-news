import json

from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, abort, Response
from flask.views import MethodView, View
from flask_login import login_required, current_user
from news_website import db
from news_website.models import News, newsCategory, journalistNewsMapping, newsImageMapping, User
from news_website.news.forms import PostArticlesForm, ArticlesImageUploadForm, UpdateArticlesForm
import datetime
import os
from news_website.news.utils import allowed_file

news = Blueprint("news", __name__)


class postArticlesPage(MethodView):
    """function for posting articles by journalist"""

    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            return render_template('post_article.html', form=PostArticlesForm(), categories=newsCategory.query.all(),
                                   form1=ArticlesImageUploadForm())
        else:
            abort(403)

    def post(self, user_id):
        form = PostArticlesForm()
        form1 = ArticlesImageUploadForm()
        categories = newsCategory.query.all()
        if form.validate_on_submit() and form1.validate_on_submit():
            for file in form1.picture.data:
                if not allowed_file(file.filename):
                    flash('Please select valid extensions such as jpg, png or jpeg', 'warning')
                    return render_template('post_article.html', form=form, form1=form1, categories=categories)
            post = News(news_heading=form.title.data, news_info=form.content.data, news_date=datetime.datetime.now(),
                        is_approved=False, news_category_id=request.form.get('category'))
            db.session.add(post)
            db.session.commit()

            journalist_news = journalistNewsMapping(journalist_id=current_user.id, news_id=post.news_id)
            db.session.add(journalist_news)
            db.session.commit()

            for file in form1.picture.data:
                if file.filename:
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
                    news_image = newsImageMapping(news_id=post.news_id, image=file.filename)
                    db.session.add(news_image)
                    db.session.commit()

            flash('Your article has been successfully sent to admin to get verified.', 'success')
            # return redirect(url_for('home_page'))
            return redirect(url_for('show_journalist_article_page', user_id=user_id))


class showJournalistArticles(MethodView):
    """class for showing articles posted by journalist"""

    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            journalist_news_id_list = User.query \
                .join(journalistNewsMapping, User.id == journalistNewsMapping.journalist_id) \
                .add_columns(journalistNewsMapping.news_id) \
                .filter(User.id == current_user.id).all()
            news_dict = {}
            images_dict = {}
            for articles in journalist_news_id_list:
                news_list = News.query.filter_by(news_id=articles[1]).first()
                images_list = newsImageMapping.query.filter_by(news_id=articles[1]).all()
                news_dict[news_list.news_id] = news_list
                images_dict[news_list.news_id] = []
                for one_image in images_list:
                    image_file = url_for('static', filename='news_images/' + one_image.image)
                    images_dict[news_list.news_id].append(image_file)

            return render_template('show_journalist_article.html', news_dict=news_dict, images_dict=images_dict)
        else:
            abort(403)


class updateArticlesPage(MethodView):
    """class for updating articles posted by journalist"""

    decorators = [login_required]

    def get(self, user_id, news_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            form = UpdateArticlesForm()
            news_data = News.query.filter_by(news_id=news_id).first()
            image_data = newsImageMapping.query.filter_by(news_id=news_id).all()
            form.title.data = news_data.news_heading
            form.content.data = news_data.news_info
            image_list = []
            for images in image_data:
                image_list.append({
                    "image_url": url_for('static', filename='news_images/' + images.image),
                    "news_id": images.news_id,
                    "image": images.image
                })

            return render_template("update_articles.html", form=form, categories=newsCategory.query.all(),
                                   category_id=news_data.news_category_id, image_list=image_list)
        else:
            abort(403)

    def post(self, news_id, user_id):
        form = UpdateArticlesForm()
        if form.validate_on_submit():
            news_data = News.query.filter_by(news_id=news_id).first()
            news_data.news_heading = form.title.data
            news_data.news_info = form.content.data
            news_data.news_category_id = request.form.get('category')
            images_data_obj = newsImageMapping.query.filter_by(news_id=news_id).all()
            images_data = []
            for img in images_data_obj:
                images_data.append(img.image)

            for file in form.picture.data:
                if not allowed_file(file.filename):
                    flash('Please select valid extensions such as jpg, png or jpeg', 'warning')
                    # return render_template('update_articles.html', form=form, categories=newsCategory.query.all())
                    return redirect(url_for('update_article', news_id=news_id, user_id=user_id))
                elif file.filename in images_data:
                    flash('Image with this name already exists please select different image or change the name of the image', 'warning')
                    return redirect(url_for('update_article', news_id=news_id, user_id=user_id))

        for file in form.picture.data:
            if file.filename:
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
                news_image = newsImageMapping(news_id=news_id, image=file.filename)
                db.session.add(news_image)
                db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('show_journalist_article_page', user_id=current_user.id))


class DeleteArticles(MethodView):
    """class for deleting articles by journalist"""

    decorators = [login_required]

    def get(self, user_id, news_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            journalist_news_object = journalistNewsMapping.query.filter_by(news_id=news_id).first()
            news_image_object = newsImageMapping.query.filter_by(news_id=news_id).first()
            news_object = News.query.filter_by(news_id=news_id).first()
            db.session.delete(journalist_news_object)
            if news_image_object:
                db.session.delete(news_image_object)
            db.session.delete(news_object)
            db.session.commit()
            return {"success": True, "message": "Article deleted"}
        else:
            abort(403)


class DeleteArticlesImage(MethodView):
    """class for deleting articles image by journalist"""

    decorators = [login_required]

    def post(self):
        post_data = request.json
        news_id = post_data.get("news_id")
        journalist_obj = journalistNewsMapping.query.filter_by(news_id=news_id).scalar()
        if journalist_obj.journalist_id == current_user.id and current_user.usertype.type == "journalist":
            image_txt = post_data.get("image_txt")

            news_image_mapping = newsImageMapping.query.filter(newsImageMapping.news_id == news_id,
                                                               newsImageMapping.image == image_txt).scalar()
            db.session.delete(news_image_mapping)
            db.session.commit()

            return {"success": True}
        else:
            abort(403)
