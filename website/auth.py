from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Password


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # passwords = Password.query.all()
    # passwords_text = []

    passwords = []
    passwords_text = []

    for p in passwords:
        passwords_text.append(p.password)

    if request.method == 'POST':
        parola = request.form.get('password_public')
        if parola in passwords_text:
            session['parola'] = parola
            return redirect(url_for('views.voting'))
        else:
            session['error_voting'] = 'Incorrect password. Please Try again!'
            return redirect(url_for('views.error'))

    return render_template("login.html")