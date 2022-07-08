import unittest
import pytest
# from flask_testing import TestCase

from run import app


class TestNotRenderTemplates(unittest.TestCase):

    def setUp(self):
        super(TestNotRenderTemplates, self).setUp()
        self.app = app.test_client()
        # return app.test_client()
    # def create_app(self):
    #     super(TestNotRenderTemplates, self).create_app()
    #     self.app = app.test_client()
    #     # return app.test_client()

    def test_assert_my_template_used(self):
        res = self.app.get('/')

        print(res)
        # self.assert_template_used('home.html', res)
        # self.assert_context("greeting", "hello")
        # response = self.client.get("/journalist_articles")
        #
        # self.assert_template_used('journalist_articles.html')


# def test_execute(client):
#     article_data = client.get("/journalist_articles")
#     print(f"article_data.headers['Location'] --- {article_data.headers['Location']}")
# assert 'http://localhost/auth/login' == article_data.headers['Location']
# self.assert_template_used(article_data, 'journalist_articles.html')

