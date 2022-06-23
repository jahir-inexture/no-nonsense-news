from news_website import create_app, db
from flask_migrate import Migrate

from news_website.admin.routes import checkArticlesPage, approveArticle, declineArticle, showAllArticles, \
    showArticlesByJournalist, addCategory, deleteCategory
from news_website.main.routes import HomePage
from news_website.users.routes import LoginPage, RegistrationPage, ProfilePage, Logout, ResetPasswordRequest, \
    ResetToken, ChangePasswordPage
from news_website.news.routes import PostArticlesPage, ShowJournalistArticles, UpdateArticlesPage, DeleteArticles, \
    DeleteArticlesImage

app = create_app()
migrate = Migrate(app, db)

# urls for home page
app.add_url_rule('/', view_func=HomePage.as_view('home'))
app.add_url_rule('/home', view_func=HomePage.as_view('home_page'))

# urls for users
app.add_url_rule('/login', view_func=LoginPage.as_view('login_page'))
app.add_url_rule('/registration', view_func=RegistrationPage.as_view('registration_page'))
app.add_url_rule('/profile/<int:user_id>', view_func=ProfilePage.as_view('profile_page'))
app.add_url_rule('/Logout', view_func=Logout.as_view('Logout'))
app.add_url_rule('/reset_password', view_func=ResetPasswordRequest.as_view('reset_password_request'))
app.add_url_rule('/reset_password/<token>', view_func=ResetToken.as_view('reset_token'))
app.add_url_rule('/change_password', view_func=ChangePasswordPage.as_view('change_password_page'))

# urls for news
app.add_url_rule('/post_articles/<int:user_id>', view_func=PostArticlesPage.as_view('post_article_page'))
app.add_url_rule('/show_journalist_articles/<int:user_id>',
                 view_func=ShowJournalistArticles.as_view('show_journalist_article_page'))
app.add_url_rule('/show_journalist_articles/<int:user_id>/update_article/<int:news_id>',
                 view_func=UpdateArticlesPage.as_view('update_article'))

app.add_url_rule('/delete_article/<int:user_id>/<int:news_id>',
                 view_func=DeleteArticles.as_view('delete_article'))

app.add_url_rule('/remove_image',
                 view_func=DeleteArticlesImage.as_view('delete_article_image'))

# urls for admin
app.add_url_rule('/admin/check_article/<int:user_id>', view_func=checkArticlesPage.as_view('check_articles'))
app.add_url_rule('/admin/approve/<int:user_id>/<int:news_id>', view_func=approveArticle.as_view('approve_article'))
app.add_url_rule('/admin/decline//<int:user_id>/<int:news_id>', view_func=declineArticle.as_view('decline_article'))
app.add_url_rule('/admin/show_all_articles/<int:user_id>',
                 view_func=showAllArticles.as_view('show_all_articles'))
app.add_url_rule('/admin/show_articles_by_journalist/<int:user_id>/<int:journalist_id>',
                 view_func=showArticlesByJournalist.as_view('show_articles_by_journalist'))
app.add_url_rule('/admin/add_category/<int:user_id>', view_func=addCategory.as_view('add_category'))
app.add_url_rule('/admin/delete_category/<int:user_id>/<int:categoryId>',
                 view_func=deleteCategory.as_view('delete_category'))

if __name__ == '__main__':
    app.run(debug=True)
