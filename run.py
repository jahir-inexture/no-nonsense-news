from news_website import create_app, db
from flask_migrate import Migrate
from news_website.main.routes import homePage
from news_website.users.routes import loginPage, registrationPage, profilePage, logout, resetPasswordRequest, \
    resetToken, changePasswordPage
from news_website.news.routes import postArticlesPage, showJournalistArticles, updateArticlesPage, DeleteArticles, DeleteArticlesImage

app = create_app()
migrate = Migrate(app, db)

# urls for home page
app.add_url_rule('/', view_func=homePage.as_view('home'))
app.add_url_rule('/home', view_func=homePage.as_view('home_page'))

# urls for users
app.add_url_rule('/login', view_func=loginPage.as_view('login_page'))
app.add_url_rule('/registration', view_func=registrationPage.as_view('registration_page'))
app.add_url_rule('/profile/<int:user_id>', view_func=profilePage.as_view('profile_page'))
app.add_url_rule('/logout', view_func=logout.as_view('logout'))
app.add_url_rule('/reset_password', view_func=resetPasswordRequest.as_view('reset_password_request'))
app.add_url_rule('/reset_password/<token>', view_func=resetToken.as_view('reset_token'))
app.add_url_rule('/change_password', view_func=changePasswordPage.as_view('change_password_page'))

# urls for news
app.add_url_rule('/post_articles/<int:user_id>', view_func=postArticlesPage.as_view('post_article_page'))
app.add_url_rule('/show_journalist_articles/<int:user_id>',
                 view_func=showJournalistArticles.as_view('show_journalist_article_page'))
app.add_url_rule('/show_journalist_articles/<int:user_id>/update_article/<int:news_id>',
                 view_func=updateArticlesPage.as_view('update_article'))

app.add_url_rule('/delete_article/<int:user_id>/<int:news_id>',
                 view_func=DeleteArticles.as_view('delete_article'))

app.add_url_rule('/remove_image',
                 view_func=DeleteArticlesImage.as_view('delete_article_image'))

if __name__ == '__main__':
    app.run(debug=True)
