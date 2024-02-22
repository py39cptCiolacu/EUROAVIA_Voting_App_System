from views import views_blueprint as views
from flask import session, render_template

@views.route('/error', methods=['GET', 'POST'])
def error():

	error_vot = session['error_voting']

	return render_template("error.html", text = error_vot)