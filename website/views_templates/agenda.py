from views import views_blueprint as views
from models import Agenda
from flask import render_template

@views.route('/agenda', methods=['GET', 'POST'])
def agenda():

    agenda_text = Agenda.query.order_by(Agenda.id.desc()).first().agenda
    agenda_split = agenda_text.split(';')

    return render_template("agenda.html", agenda_split=agenda_split)