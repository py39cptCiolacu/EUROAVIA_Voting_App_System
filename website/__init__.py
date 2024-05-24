from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "baza.db"

def create_app():

	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'ApK-VoTaRe-DeBaTeX'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

	db.init_app(app)

	from .auth import auth_blueprint
	from .views import views_blueprint
	from .admin import admin_blueprint

	app.register_blueprint(views_blueprint, url_prefix='/')
	app.register_blueprint(auth_blueprint, url_prefix='/')
	app.register_blueprint(admin_blueprint, url_prefix='/admin-panel')

	create_database(app)

	from .models import Admin

	login_manager = LoginManager()
	login_manager.login_view = 'views.admin_log_in'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return Admin.query.get(int(id))
    
	
	return app

def create_database(app):
	with app.app_context():
		db.create_all()
