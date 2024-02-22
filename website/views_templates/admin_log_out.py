from views import views_blueprint as views
from flask_login import login_required, logout_user
from flask import redirect, url_for


@views.route('/admin_log_out', methods=['GET', 'POST'])
@login_required
def admin_log_out():
    logout_user()
    return redirect(url_for('views.admin'))