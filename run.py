from news_website import create_app, db
from flask_migrate import Migrate
from news_website.main.routes import homePage
from news_website.users.routes import loginPage, registrationPage, profilePage, logout, resetPasswordRequest, resetToken

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


if __name__ == '__main__':
    app.run(debug=True)
