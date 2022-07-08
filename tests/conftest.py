import os

import pytest
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
bcrypt = Bcrypt()


# @pytest.fixture(scope="function")
def create_db():
    app = Flask(__name__)
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI')
    db.init_app(app)
    bcrypt.init_app(app)

    migrate = Migrate(app, db)

    # from news_website.users.routes import users
    # from news_website.main.routes import main
    # from news_website.news.routes import news
    # from news_website.errors.handlers import errors
    # from news_website.admin.routes import admin
    # from news_website.public.routes import public
    # app.register_blueprint(users)
    # app.register_blueprint(main)
    # app.register_blueprint(news)
    # app.register_blueprint(errors)
    # app.register_blueprint(admin)
    # app.register_blueprint(public)

    return app


@pytest.fixture(scope="session")
def client():
    app = create_db()
    return app.test_client()
