from views import views_blueprint as views
from flask import render_template
from flask_login import login_required
from models import Status, Votes, Motion, Password


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
