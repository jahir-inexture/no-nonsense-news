import cloudinary
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, abort
from flask.views import MethodView
from flask_login import login_required, current_user
from news_website import db
from news_website.models import News, NewsCategory, JournalistNewsMapping, NewsImageMapping, User
from news_website.news.forms import PostArticlesForm, ArticlesImageUploadForm, UpdateArticlesForm, UploadFileForm
import datetime
from news_website.news.utils import allowed_file
import cloudinary.uploader

news = Blueprint("news", __name__)

# cloudinary.config(
#     cloud_name="dgegns1en",
#     api_key="211425158599682",
#     api_secret="W2GdbxRYJvljDMrMq3k6jYPjyxM"
# )


class PostArticlesPage(MethodView):
    """function for posting articles by journalist"""

    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            return render_template('post_article.html', form=PostArticlesForm(), categories=NewsCategory.query.all(),
                                   form1=ArticlesImageUploadForm())
        else:
            abort(403)

    def post(self, user_id):
        form = PostArticlesForm()
        form1 = ArticlesImageUploadForm()
        categories = NewsCategory.query.all()
        if form.validate_on_submit() and form1.validate_on_submit():
            for file in form1.picture.data:
                if not allowed_file(file.filename):
                    flash('Please select valid extensions such as jpg, png, jpeg or webp', 'warning')
                    return render_template('post_article.html', form=form, form1=form1, categories=categories)
            post = News(news_heading=form.title.data, news_info=form.content.data, news_date=datetime.datetime.now(),
                        checked=False, news_category_id=request.form.get('category'), scraped_data=False)
            db.session.add(post)
            db.session.commit()

            journalist_news = JournalistNewsMapping(journalist_id=current_user.id, news_id=post.news_id)
            db.session.add(journalist_news)
            db.session.commit()

            for file in form1.picture.data:
                if file.filename:
                    upload_result = cloudinary.uploader.upload(file, folder="News_Website")
                    news_image = NewsImageMapping(news_id=post.news_id, image=upload_result['url'])
                    db.session.add(news_image)
                    db.session.commit()

            flash('Your article has been successfully sent to admin to get verified.', 'success')
            return redirect(url_for('show_journalist_article_page', user_id=user_id))


class ShowJournalistArticles(MethodView):
    """class for showing articles posted by journalist"""

    decorators = [login_required]

    def get(self, user_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            page = request.args.get('page', 1, type=int)

            journalist_news_id_list = User.query \
                .join(JournalistNewsMapping, User.id == JournalistNewsMapping.journalist_id) \
                .add_columns(JournalistNewsMapping.news_id) \
                .filter(User.id == current_user.id).paginate(page=page, per_page=5)
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


class UpdateArticlesPage(MethodView):
    """class for updating articles posted by journalist"""

    decorators = [login_required]

    def get(self, user_id, news_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            form = UpdateArticlesForm()
            news_data = News.query.filter_by(news_id=news_id).first()
            image_data = NewsImageMapping.query.filter_by(news_id=news_id).all()
            form.title.data = news_data.news_heading
            form.content.data = news_data.news_info
            image_list = []
            for images in image_data:
                image_list.append({
                    "image_url": images.image,
                    "news_id": images.news_id,
                    "image": images.image
                })

            return render_template("update_articles.html", form=form, categories=NewsCategory.query.all(),
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

            for file in form.picture.data:
                if not allowed_file(file.filename):
                    flash('Please select valid extensions such as jpg, png, jpeg or webp', 'warning')
                    return redirect(url_for('update_article', news_id=news_id, user_id=user_id))

            for file in form.picture.data:
                if file.filename:
                    upload_result = cloudinary.uploader.upload(file, folder="News_Website")
                    news_image = NewsImageMapping(news_id=news_id, image=upload_result['url'])
                    db.session.add(news_image)
                    db.session.commit()
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('show_journalist_article_page', user_id=current_user.id))


class DeleteArticles(MethodView):
    """class for deleting articles by journalist"""

    decorators = [login_required]

    def get(self, user_id, news_id):
        if user_id == current_user.id and current_user.usertype.type == "journalist":
            journalist_news_object = JournalistNewsMapping.query.filter_by(news_id=news_id).first()
            news_image_object = NewsImageMapping.query.filter_by(news_id=news_id).first()
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
        journalist_obj = JournalistNewsMapping.query.filter_by(news_id=news_id).scalar()
        if journalist_obj.journalist_id == current_user.id and current_user.usertype.type == "journalist":
            image_txt = post_data.get("image_txt")

            news_image_mapping = NewsImageMapping.query.filter(NewsImageMapping.news_id == news_id,
                                                               NewsImageMapping.image == image_txt).scalar()
            db.session.delete(news_image_mapping)
            db.session.commit()

            return {"success": True}
        else:
            abort(403)

