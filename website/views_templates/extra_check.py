from views import views_blueprint as views
from flask import redirect, session, url_for
from models import Votes

@views.route('/extra_check', methods = ['GET', 'POST'])
def extra_check():
        
        password = session['parola']
        check = Votes.query.filter_by(password=password).first()
        if check:
            return redirect(url_for('views.congrats'))
        else:
            session['error_voting'] = 'Unexpected Error. Please Vote Again'
            return redirect(url_for('views.error'))
