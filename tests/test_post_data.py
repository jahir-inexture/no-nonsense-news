# from unittest import TestCase
from flask_testing import TestCase
from flask import url_for

from run import app
from news_website import create_app, db, bcrypt
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


    def test_login_success(self):
        form = LoginForm()
        form.email.data = 'test1@t1.ni'
        form.password.data = 'Test@123'
        data = form.data
        print(data)
        res = self.client.post('/login', data=data, follow_redirects=False)
        
        # print(res.get_data(as_text=True))

        # self.assert_message_flashed('Login Failed, Please try again', 'danger')
        # self.assert_message_flashed('Login Unsuccessful. Please check email and password', 'danger')

        self.assert_message_flashed('Login Successful', 'success')
        self.assertEqual(res.status_code, 302)
        # self.assertRedirects(res.location, url_for('home_page'))
        # self.assert_redirects(res, '/home')
        

    def test_login_fail_invalid_credantials(self):
        form = LoginForm()
        form.email.data = 'test1@t1.in'
        form.password.data = 'Test@123'
        data = form.data
        print(data)
        res = self.client.post('/login', data=data, follow_redirects=False)
        
        # print(res.get_data(as_text=True))

        # self.assert_message_flashed('Login Failed, Please try again', 'danger')
        self.assert_message_flashed('Login Unsuccessful. Please check email and password', 'danger')
        self.assert_template_used('login.html')

