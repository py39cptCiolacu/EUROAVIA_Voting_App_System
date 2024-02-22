from views import views_blueprint as views
from flask_login import login_required
from flask import render_template, request, redirect, url_for
from .. import db
from models import Votes, Motion


@views.route('/admin_reset', methods=['GET', 'POST'])
@login_required
def admin_reset():

    if request.method == 'POST':
        reset = request.form.get('reset')
        if reset == 'RESET-DATABASE':
            Votes.query.delete()
            # Password.query.delete()
            motion = Motion(motion='no motion right now!')
            db.session.add(motion)
            db.session.commit()
            return redirect(url_for('views.admin'))

    return render_template("admin_reset.html")