from dotenv import load_dotenv
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from news_website.config import Config
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

load_dotenv()

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from news_website.users.routes import users
    from news_website.main.routes import main
    from news_website.news.routes import news
    from news_website.errors.handlers import errors
    from news_website.admin.routes import admin
    from news_website.public.routes import public
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(news)
    app.register_blueprint(errors)
    app.register_blueprint(admin)
    app.register_blueprint(public)

    return app
