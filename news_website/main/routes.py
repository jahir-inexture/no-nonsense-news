from flask import Blueprint, render_template
from flask.views import MethodView
from news_website.main.utils import get_latest_news_for_home_page
from news_website.models import News

main = Blueprint("main", __name__)


class HomePage(MethodView):
    """Class for getting the home page for the website"""

    def get(self):
        latest_journalist_news = News.query.filter_by(scraped_data=False, is_approved=True).order_by(
            News.news_date.desc()).limit(5).all()
        politics_dict, politics = get_latest_news_for_home_page("Politics")
        main_politics = politics[0]
        other_politics = politics[1:]

        entertainment_dict, entertainment = get_latest_news_for_home_page("Entertainment")
        main_entertainment = entertainment[0]
        other_entertainment = entertainment[1:]

        sports_dict, sports = get_latest_news_for_home_page("Sports")
        main_sports = sports[0]
        other_sports = sports[1:]

        education_dict, education = get_latest_news_for_home_page("Education")
        main_education = education[0]
        other_education = education[1:]

        return render_template('home.html', latest_journalist_news=latest_journalist_news,
                               main_politics=main_politics, other_politics=other_politics, politics_dict=politics_dict,
                               main_entertainment=main_entertainment, other_entertainment=other_entertainment,
                               entertainment_dict=entertainment_dict,
                               main_sports=main_sports, other_sports=other_sports, sports_dict=sports_dict,
                               main_education=main_education, other_education=other_education,
                               education_dict=education_dict)
