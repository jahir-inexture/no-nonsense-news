import scrapy
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from news_website import db
from news_website.models import News, NewsCategory, NewsImageMapping
from run import app


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
            if self.change_date_format(news.css('div.articles div.date::text').get()).date() == datetime.today().date():
                a = {
                    'heading': news.css('h2.title a::text').get(),
                    'content': news.css('div.articles p::text').get(),
                    'date': self.change_date_format(news.css('div.articles div.date::text').get()),
                    'image': news.css('div.articles a img').attrib['data-lazy-src']
                }
                # yield a
                if not self.check_existing_news(a['heading']):
                    with app.app_context():
                        news = News(news_heading=a['heading'], news_info=a['content'],
                                    news_date=a['date'],
                                    news_category_id=self.category_obj.category_id, scraped_data=True)
                        db.session.add(news)
                        db.session.commit()
                        news_image = NewsImageMapping(news_id=news.news_id, image=a['image'])
                        db.session.add(news_image)
                        db.session.commit()

        next_page = response.css('a.next.page-numbers').attrib['href']
        if self.page_number < 5:
            yield response.follow(next_page, callback=self.parse)

    def change_date_format(self, raw_date):
        """function for change string into datetime object"""

        date_list = raw_date.split()
        date_str = f"{date_list[2]}/{date_list[0]}/{date_list[1][:-1]} {date_list[3]} {date_list[4]}"
        date_obj = datetime.strptime(date_str, '%Y/%B/%d %I:%M:%S %p')
        return date_obj

    def check_existing_news(self, news_data):
        with app.app_context():
            news_obj = News.query.filter_by(news_heading=news_data).first()
            if news_obj:
                return True
            else:
                return False


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(PoliticsSpider)
    process.start()
