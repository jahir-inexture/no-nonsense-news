import sys
import scrapy
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner

from news_website import db
from news_website.models import News, NewsCategory, NewsImageMapping
from run import app


def change_date_format(raw_date):
    """function for change string into datetime object"""
    date_list = raw_date.split()
    date_str = f"{date_list[2]}/{date_list[0]}/{date_list[1][:-1]} {date_list[3]} {date_list[4]}"
    date_obj = datetime.strptime(date_str, '%Y/%B/%d %I:%M:%S %p')
    return date_obj


def check_existing_news(news_data):
    """function for checking if the data exists or not in the database"""
    with app.app_context():
        news_obj = News.query.filter_by(news_heading=news_data).first()
        if news_obj:
            return True
        else:
            return False


def insert_data(category_obj, data):
    """function for inserting news into the database"""
    with app.app_context():
        news = News(news_heading=data['heading'], news_info=data['content'],
                    news_date=data['date'],
                    news_category_id=category_obj.category_id, scraped_data=True)
        db.session.add(news)
        db.session.commit()
        news_image = NewsImageMapping(news_id=news.news_id, image=data['image'])
        db.session.add(news_image)
        db.session.commit()


class PoliticsSpider(scrapy.Spider):
    name = "politics"
    start_urls = ['https://indianexpress.com/section/political-pulse/']
    page_number = 0
    with app.app_context():
        category_obj = NewsCategory.query.filter_by(category="Politics").first()

    def parse(self, response):
        """function for parsing data"""

        self.page_number += 1
        for news in response.css('div.articles'):
            if change_date_format(news.css('div.articles div.date::text').get()).date() == datetime.today().date():
                data = {
                    'heading': news.css('h2.title a::text').get(),
                    'content': news.css('div.articles p::text').get(),
                    'date': change_date_format(news.css('div.articles div.date::text').get()),
                    'image': news.css('div.articles a img').attrib['data-lazy-src']
                }
                if not check_existing_news(data['heading']):
                    insert_data(self.category_obj, data)

        next_page = response.css('a.next.page-numbers').attrib['href']
        if self.page_number < 5:
            yield response.follow(next_page, callback=self.parse)


class EntertainmentSpider(scrapy.Spider):
    name = "entertainment"
    start_urls = ['https://indianexpress.com/section/entertainment/']
    page_number = 0
    with app.app_context():
        category_obj = NewsCategory.query.filter_by(category="Entertainment").first()

    def parse(self, response):
        """function for parsing data"""

        self.page_number += 1
        for news in response.css('div.articles'):
            if change_date_format(news.css('div.articles div.date::text').get()).date() == datetime.today().date():
                data = {
                    'heading': news.css('div.title a::text').get(),
                    'content': news.css('div.articles p::text').get(),
                    'date': change_date_format(news.css('div.articles div.date::text').get()),
                    'image': news.css('div.articles a img').attrib['data-lazy-src']
                }
                if not check_existing_news(data['heading']):
                    insert_data(self.category_obj, data)

        next_page = response.css('a.next.page-numbers').attrib['href']
        if self.page_number < 5:
            yield response.follow(next_page, callback=self.parse)


class SportsSpider(scrapy.Spider):
    name = "sports"
    start_urls = ['https://indianexpress.com/section/sports/']
    page_number = 0
    with app.app_context():
        category_obj = NewsCategory.query.filter_by(category="Sports").first()

    def parse(self, response):
        """function for parsing data"""

        self.page_number += 1
        for news in response.css('div.articles'):
            if change_date_format(news.css('div.articles div.date::text').get()).date() == datetime.today().date():
                data = {
                    'heading': news.css('h2.title a::text').get(),
                    'content': news.css('div.articles p::text').get(),
                    'date': change_date_format(news.css('div.articles div.date::text').get()),
                    'image': news.css('div.articles a img').attrib['data-lazy-src']
                }
                if not check_existing_news(data['heading']):
                    insert_data(self.category_obj, data)

        next_page = response.css('a.next.page-numbers').attrib['href']
        if self.page_number < 5:
            yield response.follow(next_page, callback=self.parse)


class EducationSpider(scrapy.Spider):
    name = "education"
    start_urls = ['https://indianexpress.com/section/education/']
    page_number = 0
    with app.app_context():
        category_obj = NewsCategory.query.filter_by(category="Education").first()

    def parse(self, response):
        """function for parsing data"""

        self.page_number += 1
        for news in response.css('div.articles'):
            if change_date_format(news.css('div.articles div.date::text').get()).date() == datetime.today().date():
                data = {
                    'heading': news.css('h2.title a::text').get(),
                    'content': news.css('div.articles p::text').get(),
                    'date': change_date_format(news.css('div.articles div.date::text').get()),
                    'image': news.css('div.articles a img').attrib['data-lazy-src']
                }
                if not check_existing_news(data['heading']):
                    insert_data(self.category_obj, data)

        next_page = response.css('a.next.page-numbers').attrib['href']
        if self.page_number < 5:
            yield response.follow(next_page, callback=self.parse)


runner = CrawlerRunner()


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(PoliticsSpider)
    yield runner.crawl(EntertainmentSpider)
    reactor.stop()


if __name__ == "__main__":
    process = CrawlerProcess()
    class_list = [PoliticsSpider, EntertainmentSpider, SportsSpider, EducationSpider]
    for class_name in class_list:
        if "twisted.internet.reactor" in sys.modules:
            del sys.modules["twisted.internet.reactor"]
        process.crawl(class_name)
        process.start()
