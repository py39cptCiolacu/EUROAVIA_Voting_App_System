from flask import Blueprint, render_template, session, redirect, url_for
from .models import Status
from models import Agenda, Votes


views_blueprint = Blueprint('views', __name__)


def status():

    status = Status.query.order_by(Status.id.desc()).first()

    return status.status


@views_blueprint.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")


@views_blueprint.route('/agenda', methods=['GET', 'POST'])
def agenda():

    "DEV: I should be able to upload a .docx file"

    agenda_text = Agenda.query.order_by(Agenda.id.desc()).first().agenda
    agenda_split = agenda_text.split(';')

    return render_template("agenda.html", agenda_split=agenda_split)


@views_blueprint.route('/congrats', methods=['GET', 'POST'])
def congrats():

    return render_template("congrats.html")


@views_blueprint.route('/error', methods=['GET', 'POST'])
def error():

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
        

