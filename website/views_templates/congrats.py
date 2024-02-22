from views import views_blueprint as views
from flask import render_template

@views.route('/congrats', methods=['GET', 'POST'])
def congrats():

    return render_template("congrats.html")