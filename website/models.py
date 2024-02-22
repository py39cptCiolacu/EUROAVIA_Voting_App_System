from website.__init__ import db
from flask_login import UserMixin


class Votes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    vote = db.Column(db.String(150))
    password = db.Column(db.String(150))


class Motion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    motion = db.Column(db.String(1500))

    
class Password(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(10))


class Status(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(30))


class Agenda(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    agenda = db.Column(db.String())

	
class Admin(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20))
	password = db.Column(db.String(20))