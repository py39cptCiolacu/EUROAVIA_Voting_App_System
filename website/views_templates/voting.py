from views import views_blueprint as views
from views import status
from flask import render_template, request, redirect, session, url_for
from models import Motion, Votes
from .. import db 

@views.route('/voting', methods=['GET', 'POST'])
def voting():

    motion = Motion.query.order_by(Motion.id.desc()).first()

    if request.method == 'POST':
        vote_value = request.form.get('button')
        password = session['parola']
        check = Votes.query.filter_by(password=password).first()
        if check:
            session['error_voting'] = 'You already voted!'
            return redirect(url_for('views.error'))
        elif status() == 'STOP':
            session['error_voting'] = 'Sorry. Is not voting time'
            return redirect(url_for('views.error'))
        else:
            vote = Votes(vote=vote_value, password=password)
            db.session.add(vote)
            db.session.commit()
            return redirect(url_for('views.extra_check')) 

    return render_template("voting.html", motion=motion)