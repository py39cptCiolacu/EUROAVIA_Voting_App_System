from views import views_blueprint as views
from flask_login import login_required
from flask import request, render_template, flash, redirect, url_for
from models import Agenda
from .. import db

@views.route('/admin_agenda', methods=['GET', 'POST'])
@login_required
def admin_agenda():

    if request.method == 'POST':
        agenda_text = request.form.get('agenda')
        agenda = Agenda(agenda=agenda_text)
        db.session.add(agenda)
        db.session.commit()
        flash("Agenda set!")
        return redirect(url_for('views.admin'))

    return render_template("admin_agenda.html")