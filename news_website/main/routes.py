from flask import Blueprint, render_template
from flask.views import MethodView

main = Blueprint("main", __name__)


# @main.route('/')
# @main.route('/home')
# def home_page():
#     return render_template('home.html')

class homePage(MethodView):
    """Class for getting the home page for the website"""

    def get(self):
        return render_template('home.html')
