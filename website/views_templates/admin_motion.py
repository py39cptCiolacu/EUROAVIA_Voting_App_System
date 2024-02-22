from views import views_blueprint as views
from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required
from .. import db
from models import Motion

@views.route('/admin_motion', methods=['GET', 'POST'])
@login_required
def admin_motion():

    if request.method == 'POST':
        motion_text = request.form.get('motion')
        motion = Motion(motion=motion_text)
        db.session.add(motion)
        db.session.commit()
        flash("----------------Motion set!")
        return redirect(url_for('views.admin'))

    return render_template("admin_motion.html")