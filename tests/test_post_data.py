# from unittest import TestCase
from flask_testing import TestCase
from flask import url_for

from run import app
from news_website import db, bcrypt
from news_website.models import User, UserType
from news_website.users.forms import LoginForm, RegistrationForm, PasswordResetRequestForm

class TestNotRenderTemplates(TestCase):
    render_templates = False

    def setUp(self):
        print("Creating test database...")
        db.create_all()

        self.user_type = UserType(type="user")
        db.session.add(self.user_type)
        db.session.commit()
        
        self.user = User(
            user_type_id=self.user_type.user_type_id, first_name="test", last_name="test",
            gender="male", email="test1@t1.ni", age="20", phone="9234567890", address="testing",
            password=bcrypt.generate_password_hash("Test@123").decode('utf-8')
        )
        db.session.add(self.user)

    def tearDown(self):
        print("Removing test database...")
        db.session.remove()
        db.drop_all()
    
    def create_app(self):
        # app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
        return app


    def test_db_create(self):
        ut = UserType.query.all()
        users = User.query.all()

        self.assertIn(self.user_type, ut)
        self.assertIn(self.user, users)
