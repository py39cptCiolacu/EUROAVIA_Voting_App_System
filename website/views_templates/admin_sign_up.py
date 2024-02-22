from views import views_blueprint as views
from flask import render_template, request, flash, redirect, url_for
from models import Admin
from flask_login import login_user, current_user
from .. import db



@views.route('/admin_sign_up', methods=['GET', 'POST'])
def admin_sign_up():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        code = request.form.get('code')

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            flash('---------------Username already exists.', category='error')
        elif password != re_password:
            flash('---------------Passwords does not coincide', category='error')
        elif code != 'EMEAC2023':
            flash('---------------Incorect unique code')
        else:
            new_admin = Admin(username=username, password=password)
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember=True)
            flash('---------------Account created!', category='success')
            return redirect(url_for('views.admin'))

    return render_template("admin_sign_up.html", user=current_user)