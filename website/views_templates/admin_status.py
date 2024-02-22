from views import views_blueprint as views
from .. import db
from flask_login import login_required
from flask import request, flash, redirect, render_template, url_for
from models import Status


@views.route('/admin_status', methods=['GET', 'POST'])
@login_required
def admin_status():

    if request.method == 'POST':
        status_text = request.form.get('status')
        status = Status(status=status_text)
        db.session.add(status)
        db.session.commit()
        flash("----------------Status updated!")
        return redirect(url_for('views.admin'))

    return render_template("admin_status.html")