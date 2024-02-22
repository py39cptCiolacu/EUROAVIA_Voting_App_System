from website.views import views_blueprint as views
from flask import render_template

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")

