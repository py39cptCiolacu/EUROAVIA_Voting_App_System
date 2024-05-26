from flask import Blueprint, render_template, session, redirect, url_for, request
from .models import Agenda, Votes, Motion, Status
from . import db


views_blueprint = Blueprint('views', __name__)


def status():

    status = Status.query.order_by(Status.id.desc()).first()

    return status.status


@views_blueprint.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")


@views_blueprint.route('/voting', methods=['GET', 'POST'])
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


@views_blueprint.route('/agenda', methods=['GET', 'POST'])
def agenda():

    #NEW FEATURE: I should be able to upload a .docx file
    #OPTIMIZATION: async* functions which upload the new agenda every time the admin push it

    agenda_text = Agenda.query.order_by(Agenda.id.desc()).first().agenda
    agenda_split = agenda_text.split(';')

    return render_template("agenda.html", agenda_split=agenda_split)


@views_blueprint.route('/congrats', methods=['GET', 'POST'])
def congrats():

    return render_template("congrats.html")


@views_blueprint.route('/error', methods=['GET', 'POST'])
def error():

	#OPTIMIZATION: raise exception and redirect to here
     
    error_vot = session['error_voting']

    return render_template("error.html", text = error_vot)


@views_blueprint.route('/extra_check', methods = ['GET', 'POST'])
def extra_check():
        
        password = session['parola']
        check = Votes.query.filter_by(password=password).first()
        if check:
            return redirect(url_for('views.congrats'))
        else:
            session['error_voting'] = 'Unexpected Error. Please Vote Again'
            return redirect(url_for('views.error'))
        

