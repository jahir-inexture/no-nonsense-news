from news_website import create_app, db
from flask_migrate import Migrate
from news_website.admin.routes import CheckArticlesPage, ApproveArticle, DeclineArticle, ShowAllArticles, \
    ShowArticlesByJournalist, AddCategory, DeleteCategory, ScrapData, ShowFilteredArticles
from news_website.main.routes import HomePage
from news_website.public.routes import ShowNews, Subscribe, GetJournalistAllArticles, \
    GetJournalistArticles, FilteredArticles, NewsLetter, Payment, Checkout
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
app.add_url_rule('/admin/check_article/<int:user_id>', view_func=CheckArticlesPage.as_view('check_articles'))
app.add_url_rule('/admin/approve/<int:user_id>/<int:news_id>', view_func=ApproveArticle.as_view('approve_article'))
app.add_url_rule('/admin/decline//<int:user_id>/<int:news_id>', view_func=DeclineArticle.as_view('decline_article'))
app.add_url_rule('/admin/show_all_articles/<int:user_id>',
                 view_func=ShowAllArticles.as_view('show_all_articles'))
app.add_url_rule('/admin/show_articles_by_journalist/<int:user_id>/<int:journalist_id>',
                 view_func=ShowArticlesByJournalist.as_view('show_articles_by_journalist'))
app.add_url_rule('/admin/add_category/<int:user_id>', view_func=AddCategory.as_view('add_category'))
app.add_url_rule('/admin/delete_category/<int:user_id>/<int:categoryId>',
                 view_func=DeleteCategory.as_view('delete_category'))
app.add_url_rule('/admin/scrap_data/<int:user_id>', view_func=ScrapData.as_view('scrap_data'))
app.add_url_rule('/admin/show_filtered_articles/<string:filter>/<int:user_id>',
                 view_func=ShowFilteredArticles.as_view('show_filtered_articles'))

# urls for public
app.add_url_rule('/news/<string:category>', view_func=ShowNews.as_view('show_news'))
app.add_url_rule('/subscribe/<int:user_id>', view_func=Subscribe.as_view('subscribe'))
app.add_url_rule('/journalist_articles', view_func=GetJournalistAllArticles.as_view('journalist_articles'))
app.add_url_rule('/journalist_articles/<int:journalist_id>',
                 view_func=GetJournalistArticles.as_view('articles_by_journalist'))
app.add_url_rule('/journalist_filtered_articles/<int:category_id>',
                 view_func=FilteredArticles.as_view('filtered_articles'))
app.add_url_rule('/newsletter/<int:user_id>', view_func=NewsLetter.as_view('newsletter'))
app.add_url_rule('/buy_subscription/payment/<int:user_id>', view_func=Payment.as_view('payment'))
app.add_url_rule('/buy_subscription/checkout/<int:user_id>', view_func=Checkout.as_view('checkout'))

if __name__ == '__main__':
    app.run(debug=True)
