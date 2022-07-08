import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """class which stores important configuration information required for different usages"""
    try:
        SECRET_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
        SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USERNAME = os.environ.get('EMAIL_USER')
        MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
        UPLOAD_FOLDER = 'news_website/static/news_images'
        CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
        API_KEY = os.environ.get('CLOUDINARY_API_KEY')
        API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')
    except KeyError:
        SECRET_KEY = 'secret'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///news_website.db'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        MAIL_SERVER = 'smtp.googlemail.com'
        MAIL_PORT = 587
        MAIL_USE_TLS = True
        MAIL_USERNAME = 'email_user'
        MAIL_PASSWORD = 'email_password'
        UPLOAD_FOLDER = 'news_website/static/news_images'
        CLOUD_NAME = 'cloud_name'
        API_KEY = 'api_key'
        API_SECRET = 'api_secret'
