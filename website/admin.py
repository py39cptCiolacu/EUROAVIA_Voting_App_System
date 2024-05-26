from flask import redirect, request, flash, url_for, render_template, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

from .models import (Status, 
                    Votes, 
                    Motion, 
                    Password, 
                    Admin, 
                    Agenda)
from . import db


admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():

    status = Status.query.order_by(Status.id.desc()).first()
    votes = Votes.query.all()

    number_of_votes, yes, no, abstention = 0, 0, 0, 0

    for vote in votes:
        number_of_votes += 1
        if vote.vote == 'yes':
            yes += 1
        elif vote.vote == 'no':
            no += 1
        elif vote.vote == 'abstention':
            abstention += 1

    motion = Motion.query.order_by(Motion.id.desc()).first()

    passwords = Password.query.all()
    if passwords:
        get_passwords = "SET - ALL GOOD"
    else:
        get_passwords = 'MUST BE SET'

    return render_template("admin.html",
                           status=status,
                           motion=motion,
                           nr_votes=number_of_votes,
                           yes=yes,
                           no=no,
                           absention=abstention,
                           get_passwords = get_passwords)


@admin_blueprint.route('/admin_log_in', methods=['GET', 'POST'])
def admin_log_in():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            if password == admin.password:
                login_user(admin, remember=True)
                return redirect(url_for('views.admin'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("admin_log_in.html")


@admin_blueprint.route('/admin_log_out', methods=['GET', 'POST'])
@login_required
def admin_log_out():
    logout_user()
    return redirect(url_for('views.admin'))


@admin_blueprint.route('/admin_sign_up', methods=['GET', 'POST'])
def admin_sign_up():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')
        code = request.form.get('code')

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            flash('Username already exists.', category='error')
        elif password != re_password:
            flash('Passwords does not coincide', category='error')
        elif code != 'EMEAC2023':
            flash('Incorect unique code')
        else:
            new_admin = Admin(username=username, password=password)
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember=True)
            flash('---------------Account created!', category='success')
            return redirect(url_for('views.admin'))

    return render_template("admin_sign_up.html", user=current_user)


@admin_blueprint.route('/admin_agenda', methods=['GET', 'POST'])
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


@admin_blueprint.route('/admin_motion', methods=['GET', 'POST'])
@login_required
def admin_motion():

    if request.method == 'POST':
        motion_text = request.form.get('motion')
        motion = Motion(motion=motion_text)
        db.session.add(motion)
        db.session.commit()
        flash("Motion set!")
        return redirect(url_for('views.admin'))

    return render_template("admin_motion.html")


@admin_blueprint.route('/admin_passwords', methods=['GET', 'POST'])
@login_required
def admin_passwords():

    passwords = []
    if request.method == 'POST':
        passwords_text = request.form.get('passwords')
        if passwords_text == 'GET-PASSWORDS':
            for p in passwords:
                db.session.add(Password(password=p))
                db.session.commit()
            return redirect(url_for('views.admin'))

    return render_template("admin_passwords.html")


@admin_blueprint.route('/admin_reset', methods=['GET', 'POST'])
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


@admin_blueprint.route('/admin_status', methods=['GET', 'POST'])
@login_required
def admin_status():

    if request.method == 'POST':
        status_text = request.form.get('status')
        status = Status(status=status_text)
        db.session.add(status)
        db.session.commit()
        flash("Status updated!")
        return redirect(url_for('views.admin'))

    return render_template("admin_status.html")
