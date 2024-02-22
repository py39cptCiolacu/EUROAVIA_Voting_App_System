from views import views_blueprint as views
from flask import redirect, request, flash, url_for, render_template
from flask_login import login_user
from models import Admin


@views.route('/admin_log_in', methods=['GET', 'POST'])
def admin_log_in():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            if password == admin.password:
                #flash('Logged in successfully!', category='success')
                login_user(admin, remember=True)
                return redirect(url_for('views.admin'))
            else:
                flash('----------------Incorrect password, try again.', category='error')
        else:
            flash('----------------Email does not exist.', category='error')

    return render_template("admin_log_in.html")