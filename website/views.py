from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from . import db
from .models import Status, Votes, Motion, Agenda, Admin, Password
from flask_login import login_user, login_required, logout_user, current_user

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
            return redirect(url_for('views.extra_check')) 

    return render_template("voting.html", motion=motion)

@views.route('/extra_check', methods = ['GET', 'POST'])
def extra_check():
        
        password = session['parola']
        check = Votes.query.filter_by(password=password).first()
        if check:
            return redirect(url_for('views.congrats'))
        else:
            session['error_voting'] = 'Unexpected Error. Please Vote Again'
            return redirect(url_for('views.error'))


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
                flash('----------------Incorrect password, try again.', category='error')
        else:
            flash('----------------Email does not exist.', category='error')

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

    passwords = Password.query.all()
    if passwords:
        get_passwords = 'YES'
    else:
        get_passwords = 'NO'

    return render_template("admin.html",
                           status=status,
                           motion=motion,
                           nr_votes=nr_votes,
                           yes=yes,
                           no=no,
                           absention=abstention,
                           get_passwords = get_passwords)


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
        flash("----------------Status updated!")
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
        flash("----------------Motion set!")
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

    # text = 'instance\codes.xls'
    # passwords = reader(text)

    passwords = ["E0@DE",
"I9#CC",
"D4$RX",
"F1$GC",
"R3%VU",
"Q1?JV",
"F4?BY",
"X4@MZ",
"F2$SN",
"C5&GA",
"R3#YH",
"C3\RQ",
"C9?ZM",
"F3!BA",
"Y9#ZF",
"R9$NO",
"M1@ZR",
"X7!DI",
"O5!ZY",
"T8&PV",
"U2@AU",
"G5?TT",
"K6@HC",
"G2?XO",
"C5!GF",
"B1?XW",
"Q8%JT",
"Q9\IS",
"M5$QP",
"Z9\DO",
"R5#FQ",
"W4\HS",
"Q2#IA",
"P3\TF",
"L8$EQ",
"P6&NA",
"K2?QW",
"Z5\BN",
"Z4&JJ",
"G0!HA",
"Q5$DT",
"A2\PK",
"F5@TQ",
"D3&YY",
"G3!BO",
"B7\JH",
"K7\VA",
"K4\QB",
"E6$LG",
"Z2$XE",
"M4$BT",
"R4\ZJ",
"I4?PA",
"J5&KR",
"E1&CZ",
"X1\MQ",
"D8@FJ",
"D1@RV",
"W6\LV",
"H1$JG",
"K7!ZA",
"J6$DM",
"L7?TV",
"U4?VP",
"I7@DP",
"Z0$WY",
"V5&ON",
"W1?XJ",
"F4$TJ",
"S1\BV",
"D3?TU",
"J1#UV",
"T1&PI",
"G0!DB",
"D5%HO",
"N9\QT",
"D0@SN",
"C7@NA",
"Q1&MW",
"Y0#BV",
"A3$NG",
"X4@OI",
"Z2\DA",
"L2\AS",
"Z6?ZC",
"H4%ZD",
"O7\KI",
"T6&AF",
"R1!ZN",
"Q6\TN",
"I0#ZB",
"U0\WF",
"W9%VA",
"N5@US",
"X6@SQ",
"U8%PA",
"D3%LS"]

    if request.method == 'POST':
        passwords_text = request.form.get('passwords')
        if passwords_text == 'GET-PASSWORDS':
            for p in passwords:
                db.session.add(Password(password=p))
                db.session.commit()
            return redirect(url_for('views.admin'))

    return render_template("admin_passwords.html")


# def reader(text):

#     passwords = pd.read_excel(text)
#     passwords_text =[]

#     for p in passwords['Parole']:
#         passwords_text.append(p)

#     return passwords_text