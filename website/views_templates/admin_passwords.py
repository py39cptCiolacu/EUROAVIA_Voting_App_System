from views import views_blueprint as views
from flask_login import login_required
from flask import request, render_template, redirect, url_for
from .. import db
from models import Password

@views.route('/admin_passwords', methods=['GET', 'POST'])
@login_required
def admin_passwords():

    # text = 'instance\codes.xls'
    # passwords = reader(text)

    passwords = ["12345", "23456", "34567"]
    if request.method == 'POST':
        passwords_text = request.form.get('passwords')
        if passwords_text == 'GET-PASSWORDS':
            for p in passwords:
                db.session.add(Password(password=p))
                db.session.commit()
            return redirect(url_for('views.admin'))

    return render_template("admin_passwords.html")