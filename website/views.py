from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from . import db
from .models import Status, Votes, Motion, Agenda, Admin, Password
from flask_login import login_user, login_required, logout_user, current_user
import pandas as pd

views = Blueprint('views', __name__)

def status():

    status = Status.query.order_by(Status.id.desc()).first()

    return status.status

@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")


@views.route('/voting', methods=['GET', 'POST'])
def voting():

    motion = Motion.query.order_by(Motion.id.desc()).first()

    if request.method == 'POST':
        vote_value = request.form.get('button')
        password = session['parola']
        check = Votes.query.filter_by(password=password).first()
        if check:
            session['error_voting'] = 'You already voted!'
            return redirect(url_for('views.error'))
        elif status() == 'STOP':
            session['error_voting'] = 'Sorry. Is not voting time'
            return redirect(url_for('views.error'))
        else:
            vote = Votes(vote=vote_value, password=password)
            db.session.add(vote)
            db.session.commit()
            return redirect(url_for('views.congrats')) 

    return render_template("voting.html", motion=motion)


@views.route('/agenda', methods=['GET', 'POST'])
def agenda():

    agenda_text = Agenda.query.order_by(Agenda.id.desc()).first().agenda
    agenda_split = agenda_text.split(';')

    return render_template("agenda.html", agenda_split=agenda_split)


@views.route('/congrats', methods=['GET', 'POST'])
def congrats():

    return render_template("congrats.html")


@views.route('/error', methods=['GET', 'POST'])
def error():

	error_vot = session['error_voting']

	return render_template("error.html", text = error_vot)

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
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("admin_log_in.html")


@views.route('/admin_log_out', methods=['GET', 'POST'])
@login_required
def admin_log_out():
    logout_user()
    return redirect(url_for('views.admin'))
    

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():

    status = Status.query.order_by(Status.id.desc()).first()

    votes = Votes.query.all()
    nr_votes, yes, no, abstention = 0, 0, 0, 0
    for v in votes:
        nr_votes += 1
        if v.vote == 'yes':
            yes += 1
        if v.vote == 'no':
            no += 1
        if v.vote == 'abstention':
            abstention += 1

    motion = Motion.query.order_by(Motion.id.desc()).first()

    return render_template("admin.html",
                           status=status,
                           motion=motion,
                           nr_votes=nr_votes,
                           yes=yes,
                           no=no,
                           absention=abstention)


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


@views.route('/admin_status', methods=['GET', 'POST'])
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


@views.route('/admin_motion', methods=['GET', 'POST'])
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


@views.route('/admin_reset', methods=['GET', 'POST'])
@login_required
def admin_reset():

    if request.method == 'POST':
        reset = request.form.get('reset')
        if reset == 'RESET-DATABASE':
            Votes.query.delete()
            Password.query.delete()
            motion = Motion(motion='no motion right now!')
            db.session.add(motion)
            db.session.commit()
            return redirect(url_for('views.admin'))

    return render_template("admin_reset.html")


@views.route('/admin_passwords', methods=['GET', 'POST'])
@login_required
def admin_passwords():

    text = '/home/napoli2022/app/codes2.xls'
    passwords = reader(text)

    if request.method == 'POST':
        passwords_text = request.form.get('passwords')
        if passwords_text == 'GET-PASSWORDS':
            for p in passwords:
                db.session.add(Password(password=p))
                db.session.commit()
            return redirect(url_for('views.admin'))

    return render_template("admin_passwords.html")


def reader(text):

    passwords = pd.read_excel(text)
    passwords_text =[]

    for p in passwords['Parole']:
        passwords_text.append(p)

    return passwords_text